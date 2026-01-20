# !/usr/bin/env python3
"""
This script adds a few niceties on top of the Blender extension builder:

- Download the wheels from the src/requirements.txt file and update the blender_manifest.toml
- Update the version in blender_manifest.toml if the Git tag is set to vMAJOR.MINOR.PATCH
- Generates a "fake" version tag if there is no Git tag set
- Includes any files/directories/globs specified in the blender_manifest.toml "parent_files" array

It requires the BLENDER environment variable to be set to the path of the Blender executable used for building,
and requires the "tomlkit" package to be installed (included in the requirements.txt file). This can be set in a
.env file in the root of the repository, or by setting the environment variable before running the script..

To use:

python3 build_release.py
"""

import tomlkit
import shutil
import pathlib
import zipfile
import subprocess
from tempfile import mkdtemp
from os import environ
import re

def get_version() -> str | None:
    try:
        my_tag = subprocess.check_output(["git", "describe", "--tags", "--exact-match", "--match", "v*"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        return my_tag[1:]
    except subprocess.CalledProcessError:
        return None

def get_fake_version(current_version: str | None = None) -> str:
    if current_version is None or not re.search(r"^\d+\.\d+\.\d+$", current_version):
        try:
            raw_tag = subprocess.check_output(["git", "describe", "--tags", "--match", "v*"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
            tag_parts = re.match(r"^v(\d+\.\d+\.\d+)-(\d+)-([a-z0-9]+)$", raw_tag)
            current_version = "0.0.0" if tag_parts is None else tag_parts.group(1)
        except subprocess.CalledProcessError:
            current_version = "0.0.0"
            pass

    hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
    parts = current_version.split(".")
    return ".".join(parts[0:2] + [str(int(parts[2]) + 1)]) + "-dev-" + hash

if environ.get("BLENDER") is None or shutil.which(environ["BLENDER"]) is None:
    raise RuntimeError(
        "BLENDER environment variable must be set to the path of the Blender executable."
    )

with open("src/blender_manifest.toml", "r") as in_file:
    manifest = tomlkit.load(in_file)

parent_files = manifest.get("build", {}).get("parent_files", [])
wheels_dir = manifest.get("build", {}).get("wheels_dir", "wheels")

# Download requirements to "wheels" directory
subprocess.run(["pip", "wheel", "-r", "requirements.txt", "-w", wheels_dir], cwd="src")

# Update the version
manifest_version = manifest["version"]
version = get_version()
fake_version = None

if version is None:
    fake_version = get_fake_version(manifest_version)
    print(f"There is no version tag on this commit, so using a temporary build version of {fake_version}")

manifest["version"] = version or fake_version

wheels = pathlib.Path("src").joinpath(wheels_dir).glob("*.whl")
manifest["wheels"] = [p.relative_to('src').as_posix() for p in wheels]

with open("src/blender_manifest.toml", "w") as out_file:
    tomlkit.dump(manifest, out_file)

try:
    temp_dir = mkdtemp()
    temp_path = pathlib.Path(temp_dir)
    print(f"Temporary generation to: {temp_dir}")

    subprocess.run([environ["BLENDER"], "--factory-startup", "--command", "extension", "build", "--verbose", "--source-dir", "src",
         "--output-dir", temp_dir])

    zips = temp_path.glob("*.zip")
    output = next(zips, None)
    if output is None:
        raise RuntimeError("The build process did not produce a file.")
    elif next(zips, None) is not None:
        raise RuntimeError("Expected a single zip file in the output directory. Found more than one.")

    with zipfile.ZipFile(output, "a") as zip_ref:
        for globulet in parent_files:
            for file in pathlib.Path(".").glob(globulet):
                print(f"+ Adding {file.relative_to('.')} to archive...")
                zip_ref.write(file, arcname=file.relative_to("."), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    shutil.move(output, ".")
finally:
    if fake_version is not None:
        with open("src/blender_manifest.toml", "w") as out_file:
            manifest["version"] = manifest_version
            tomlkit.dump(manifest, out_file)
            print(f"Restored blender_manifest.toml version to {manifest_version}")

# SuperFLEB's Blender Addon Template

https://github.com/SuperFLEB/blender-addon-template

This is a starting template for making Blender 4.5+ extension projects that includes a basic structure and a few
tricks and code snippets. It evolves as I muddle my way through. They might not all be best practices, but they're mine. 

## What's Included

* Blender 4.5+ extension structure with a `blender_manifest.toml` file and wheels and all that.
* Directories for library files (simple modules with collections of functions)
* An `__init__.py` and `lib/addon.py` with register/deregister functions...
  * Class registration via list
  * The ability to register whole modules that include a `REGISTER_CLASSES` array of their own
  * A common menu-item loader for both operators and submenus
  * A subclass for no-draw() simplified submenus
  * Support for a `can_show()` static method on operators. Like `poll()`, but hides the item instead of graying it out.
    * _Note that the `can_show()` method needs to be tested in menu and submenu `draw()` functions. It is not built in to Blender itself like `poll()` is. The check is included in the sample submenu and the `__init__.js` file._ 
* A `util` lib with some handy functions:
  * Flatten lists!
  * Wrap words!
  * Get the collections that objects are in!
  * Get operators' defaults! And reset operators' properties to defaults!
* Example code:
  * A starter Readme
  * A simple operator that doesn't do much
  * An operator with a whole bunch of panel components
  * An operator with a UIList, including sorting and filtering
  * A Preferences panel
  * An Operator panel sub-panel
  * A Properties panel (N panel)
  * A submenu
* A packager, build_release.py
  * Uses the Blender extension builder to package up the addon, plus:
    * ...allows adding extra files from the root directory, such as README and licenses
    * ...automatically downloads wheels, bundles them into a directory, and adds them to the blender_manifest.toml
  * Packs up `src`, and throws in whatever else you want
  * Uses Git v0.0.0-... semver tags to set the version number

...and (if I forgot to update this Readme) so much more!

## What's not included, that I really ought to (i.e., the to-do list)

* Make a Python script to do the setup, instead of a bunch of search/replace
* Some libs for/examples of loading external data
  * Simple, and clean-up-after-yourself loading
* Test examples (There used to be some, but they were removed because they didn't work with Blender)

## How to use it

1. Do all the Git stuff:
   * Clone it
   * Make it yours! Remove the `.git` directory, and `git init` to make a new project.
2. In your IDE/editor of choice, do a few global replaces:
   ```
        untitled_blender_addon  -> Operator prefix and some file naming
        UntitledBlenderAddon    -> Class/variable name prefix
        UNTITLED_BLENDER_ADDON  -> bl_idname prefix
        Simple Operator         -> The name for the simple operator
        UIList Operator         -> The name for the UIList demo operator
        Untitled Blender Addon  -> The full name of the addon
        Description goes here   -> Descriptions
        Name goes here          -> Your name
        {USERNAME}/{REPONAME}   -> The GitHub info for this repo
   ```
   You'll also probably want to rename some of the class and parameter names in the operators if you use them as a base.
3. Swap in the following files:
    - `README.md` (`README.SAMPLE.md`)
    - `LICENSE` (`LICENSE.(type).SAMPLE`)
    - `CONTRIBUTING.md` (`CONTRIBUTING.SAMPLE.md`)
4. Start making your Blender addon!

# build_release.py

`build_release.py` is a script that will package up your `src` directory, plus some other files, and make a ZIP archive,
ready to install. It's easily customizable and comes out-of-the-box ready to handle most projects built off this template.

## How to use it

* You'll need Python and Blender installed.
* Install the necessary dependencies for the builder script: `pip install -r requirements.txt`
* Copy the `.env.example` file to `.env` and enter the path to your Blender executable.
* Before building a release, you should update the `version` in your `blender_manifest.toml`, then Git tag the
  latest commit to that version number (using "vX.X.X" format).
  ```shell
  git tag v0.1.2
  ```
  Builds that do not have a version tag will be set to
  a version of "<major>.<minor>.<patch+1>-dev-<hash>" temporarily for the build.


Then, simply run

```shell
python build_release.py
```

and a Blender-installable ZIP file will be generated.

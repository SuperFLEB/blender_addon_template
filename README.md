# SuperFLEB's Blender Addon Template

https://github.com/SuperFLEB/blender-addon-template

This is a starting template for making Blender 4.5+ extension projects that includes a basic structure and a few
tricks and code snippets. It evolves as I muddle my way through. They might not all be best practices, but they're mine. 

## What's Included

* A structure featuring a `src` directory for packageable source.
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
  * Packs up `src`, and throws in whatever else you want
  * Uses Git tags and the bl_info to set the version number

...and (if I forgot to update this Readme) more!

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

## Necessary Customizations

Customizations can be done in the `# SETUP` section of the file. The minimum items that will need to be customized are:

* `wrap_dir` - The directory the addon will wrapped in, i.e., what directory it will be installed to.
* `output_file` - The file name of the ZIP file to be generated.

If you did all the global replaces in the list up above, though, these will already be changed.

## How to use it

Before building an actual release, you should update the `version` in your bl_info in `__init__.py`, then Git tag the
latest commit to that version number (using either "X.X.X" or "vX.X.X" format), as this is included in the file naming.

```shell
git tag 0.1.2
```

Then, simply run

```shell
python build_release.py
```

and a `name_of_project_0.1.2.zip` file will be generated, which can be installed via the Blender Add-ons manager.

## What it does

1. Uses `git` to determine the version (by tag)
2. Blows up if you forgot to update the version in your bl_info boilerplate
3. Creates a ZIP archive named `{Project name}_{Git tag name}.zip`
4. Puts everything in a directory named in the script
5. Adds all files in `src`, except...
  * Untracked files (from Git)
  * Files matching `/__pycache__/`, `/^venv/`, `/\.gitignore/`, `/^\.idea/`, and `/.blend1$/`
6. Adds "toss-in" files from outside the `src` directory:
    * `demo`, `README`, `README.md`, `LICENSE`, the `docs_support` directory, and `COPYING`, if they exist

Of course, the script is easily customizable to add exceptions and toss-ins, and to tweak file names.

## What it doesn't do

* It doesn't ignore files in `.gitignore`. You might want some of those files.
* It doesn't verify that the file is installable. You should do that.

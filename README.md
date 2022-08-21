# SuperFLEB's Blender Addon Template

https://github.com/SuperFLEB/blender-addon-template

This is a starting template for making Blender 3.1+ addon projects, that includes a basic structure and a few
tricks and code snippets. It evolves as I muddle my way through. They might not all be best practices, but they're mine. 

## What's Included

* A structure featuring a `src` directory for packageable source.
* Directories for library files (simple modules with collections of functions)
* An `__init__.py` with register/deregister functions...
  * Class registration via list
  * The ability to register whole modules that include a `REGISTER_CLASSES` array of their own
  * A common menu-item loader for both operators and submenus
* Starter unit tests
* A `util` lib with some handy functions:
  * Flatten lists!
  * Wrap words!
  * Get the collections that objects are in!
  * Get operators' defaults! And reset operators' properties to defaults!
* Example code:
  * A starter Readme
  * An operator with a whole bunch of panel components
  * An operator with a UIList, including sorting and filtering
  * A Preferences panel
  * A submenu

...and (if I forgot to update this Readme) more!

## What's not included, that I really ought to (i.e., the todo-list)

* An N-panel example
* A Properties panel example, maybe?
* Some libs for/examples of loading external data
  * Simple, and clean-up-after-yourself loading

## How to use it

1. Do all the Git stuff: Clone it off, remove the .git directory, and `git init` to make a new project.
2. In your IDE/editor of choice, do a few global replaces:
   ```
        untitled_blender_addon  -> Operator prefix and some file naming
        UntitledBlenderAddon    -> Class/variable name prefix
        Simple Operator         -> The name for the simple operator
        UIList Operator         -> The name for the UIList demo operator
        Untitled Blender Addon  -> The full name of the addon
        Description goes here   -> Descriptions
        Name goes here          -> Your name
        {USERNAME}/{REPONAME}   -> The GitHub info for this repo
   ```
   You'll also probably want to rename some of the class and parameter names in the operators if you use them as a base.
3. Swap in the `README.SAMPLE.md` file for `README.md` and customize it
4. Start making your Blender addon!

## build_release.py

`build_release.py` is a script that will package up your `src` directory, plus some other files, and make a ZIP archive,
ready to install. It's easily customizable and comes out-of-the-box ready to handle most projects.

### Necessary Customizations

Customizations can be done in the `# SETUP` section of the file. The minimum items that will need to be customized are:

* `wrap_dir` - The directory the addon will wrapped in, i.e., what directory it will be installed to.
* `output_file` - The file name of the ZIP file to be generated.

If you did all the global replaces in the list up above, these will already have to be changed.

### How to use it

Before building an actual release, you should Git tag the latest commit to a version number, as this is included in the
file naming.

```shell
git tag 0.1.2
```

Then, simply run

```shell
python build_release.py
```

and a `name_of_project_0.1.2.zip` file will be generated, which can be installed via the Blender Add-ons manager.

### What it does

1. Uses `git` to determine the version (by tag)
2. Creates a ZIP archive named `{Project name}_{Git tag name}.zip`
3. Puts everything in a directory named in the script
4. Adds all files in `src`, except...
  * Untracked files (from Git)
  * Files matching `/__pycache__/`, `/^venv/`, `/\.gitignore/`, `/^\.idea/`, and `/.blend1$/`
5. Adds "toss-in" files from outside the `src` directory:
    * `demo`, `README`, `README.md`, `LICENSE`, and `COPYING`, if they exist

Of course, the script is easily customizable to add exceptions and toss-ins, and to tweak file names.

### What it doesn't do

* It doesn't look at `.gitignore`. You might want some of those files.
* It doesn't run tests before packaging. Since it'd need to find and run the right version of Blender, 
  that's a hassle too far.
* It doesn't verify that the file is installable. You should do that.
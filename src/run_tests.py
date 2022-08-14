import bpy
import unittest
from os import path


#
# To run tests in Blender, from the Blender program directory:
# blender --factory-startup --background --python (path)/run_tests.py
#
# e.g.,
#
# blender --factory-startup --background --python 3.2/scripts/addons/untitled_blender_addon/run_tests.py
# or
# blender --factory-startup --background --python 3.2\scripts\addons\untitled_blender_addon\run_tests.py
#

loader = unittest.TestLoader()
all_tests = unittest.TestLoader().discover(path.dirname(__file__), "test_*.py", path.dirname(__file__))
unittest.TextTestRunner(verbosity=2).run(all_tests)

import bpy
from typing import Set
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator
from ..lib import pkginfo
from ..lib import a_lib

if "_LOADED" in locals():
    import importlib

    for mod in (a_lib, pkginfo,):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()


class AnOperator(Operator):
    """Description goes here"""
    bl_idname = "untitled_blender_addon.an_operator"
    bl_label = "Untitled Blender Addon"
    bl_options = {'REGISTER', 'UNDO'}

    an_int_prop: IntProperty(name="Pick a number", description="Pick a number, any number")

    @classmethod
    def poll(cls, context) -> bool:
        return True

    def draw(self, context) -> None:
        self.layout.prop(self, "an_int_prop")
        self.layout.label(text="Click OK to continue", icon="LIGHT")

    def invoke(self, context, event) -> Set[str]:
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context) -> Set[str]:
        prefs = context.preferences.addons[package_name].preferences

        def message(menu, _) -> None:
            checked = prefs["some_property"]
            was_not_was = "was" if prefs["some_property"] else "was not"
            your_number = self.an_int_prop
            menu.layout.label(text=a_lib.get_success_message(), icon="SOLO_ON")
            menu.layout.label(text=f"Your number was {your_number}. Was I right?", icon="QUESTION")
            menu.layout.label(text=f"The checkbox in the Preferences panel {was_not_was} checked",
                              icon="CHECKMARK" if checked else "X")

        bpy.context.window_manager.popup_menu(message, title="Untitled Blender Addon")
        return {'FINISHED'}


REGISTER_CLASSES = [AnOperator]

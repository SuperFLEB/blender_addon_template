import bpy
from typing import Set
from bpy.types import Operator

if "_LOADED" in locals():
    import importlib

    for mod in ():  # list all imports here
        importlib.reload(mod)
_LOADED = True


class UNTITLED_BLENDER_ADDON_OT_ASimpleOperator(Operator):
    """Description goes here"""
    bl_idname = "untitled_blender_addon.a_simple_operator"
    bl_label = "Simple Operator"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def post_register(cls):
        # Do something after registering the class in __init__.py
        pass

    @classmethod
    def post_unregister(cls):
        # Do something after unregistering the class in __init__.py
        pass

    def draw(self, context) -> None:
        # In the demo, you should NOT see this popup because the operator_context is EXEC_DEFAULT
        # and neither invoke() nor this draw() will run.
        self.layout.label(text="Invoke Screen (Was your context INVOKE_DEFAULT?)")

    def invoke(self, context, event) -> Set[str]:
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context) -> Set[str]:
        def message(menu, _) -> None:
            menu.layout.label(text="Simple operator says hello!", icon="SOLO_ON")

        bpy.context.window_manager.popup_menu(message, title="Untitled Blender Addon")
        return {'FINISHED'}


REGISTER_CLASSES = [UNTITLED_BLENDER_ADDON_OT_ASimpleOperator]

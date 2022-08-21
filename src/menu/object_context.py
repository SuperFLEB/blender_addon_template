import bpy
from ..operator import an_operator
from ..operator import an_operator_with_a_uilist

if "_LOADED" in locals():
    import importlib

    for mod in (an_operator,):  # list all imports here
        importlib.reload(mod)
_LOADED = True


class UntitledBlenderAddonSubmenu(bpy.types.Menu):
    bl_idname = 'untitled_blender_addon.untitled_blender_addon'
    bl_label = 'Untitled Blender Addon'

    def draw(self, context) -> None:
        self.layout.operator(an_operator.AnOperator.bl_idname)
        self.layout.operator(an_operator_with_a_uilist.AnOperatorWithUIList.bl_idname)


REGISTER_CLASSES = [UntitledBlenderAddonSubmenu]

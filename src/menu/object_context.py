import bpy
from ..operator import an_operator
from ..operator import an_operator_with_a_uilist

if "_LOADED" in locals():
    import importlib

    for mod in (an_operator,):  # list all imports here
        importlib.reload(mod)
_LOADED = True


class UntitledBlenderAddonSubmenu(bpy.types.Menu):
    bl_idname = 'UNTITLED_BLENDER_ADDON_MT_untitled_blender_addon_submenu'
    bl_label = 'Untitled Blender Addon'

    def draw(self, context) -> None:
        for cls in [an_operator.AnOperator, an_operator_with_a_uilist.AnOperatorWithUIList]:
            if (not hasattr(cls, 'can_show')) or cls.can_show(context):
                self.layout.operator(cls.bl_idname)


REGISTER_CLASSES = [UntitledBlenderAddonSubmenu]

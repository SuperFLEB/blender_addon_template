import bpy
from ..operator import a_simple_operator
from ..operator import an_operator
from ..operator import an_operator_with_a_uilist
from ..lib import addon

if "_LOADED" in locals():
    import importlib

    for mod in (a_simple_operator, an_operator, an_operator_with_a_uilist,):  # list all imports here
        importlib.reload(mod)
_LOADED = True


class UntitledBlenderAddonSubmenu(addon.SimpleMenu):
    bl_idname = 'UNTITLED_BLENDER_ADDON_MT_untitled_blender_addon_submenu'
    bl_label = 'Untitled Blender Addon'
    items = [
        (a_simple_operator.ASimpleOperator, "EXEC_DEFAULT"),
        an_operator.AnOperator,
        an_operator_with_a_uilist.AnOperatorWithUIList
    ]
    operator_context = "INVOKE_DEFAULT"


REGISTER_CLASSES = [UntitledBlenderAddonSubmenu]

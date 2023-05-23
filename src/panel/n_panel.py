import bpy
from bpy.types import Panel

if "_LOADED" in locals():
    import importlib

    for mod in ():  # list all imports here
        importlib.reload(mod)
_LOADED = True


class NPanel(Panel):
    bl_idname = 'VIEW3D_PT_n_panel'
    bl_category = 'Untitled Blender Addon'
    bl_label = 'Untitled Blender Addon'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        self.layout.label(text='This is an N panel')


REGISTER_CLASSES = [NPanel]

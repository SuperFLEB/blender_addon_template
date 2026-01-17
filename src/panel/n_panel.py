import bpy
from bpy.types import Panel
from ..lib import f8

f8.reload() # Reload any imports here

class VIEW3D_PT_PT_NPanel(Panel):
    bl_idname = 'VIEW3D_PT_n_panel'
    bl_category = 'Untitled Blender Addon'
    bl_label = 'Untitled Blender Addon'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        self.layout.label(text='This is an N panel')


REGISTER_CLASSES = [VIEW3D_PT_PT_NPanel]

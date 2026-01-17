import bpy
from bpy.types import Panel
from ..lib import f8

f8.reload() # Reload any imports here

class OBJECT_PT_ObjectPanel(bpy.types.Panel):
    """An example object properties panel"""
    bl_idname = "OBJECT_PT_ObjectPanel"
    bl_label = "Untitled Blender Addon"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    # Remove this if it is unnecessary
    def draw(self, context) -> None:
        layout = self.layout
        layout.label(text='This is an object panel')
        # ...


REGISTER_CLASSES = [OBJECT_PT_ObjectPanel]

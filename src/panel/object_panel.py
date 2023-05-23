import bpy
from bpy.types import Panel

if "_LOADED" in locals():
    import importlib

    for mod in ():  # list all imports here
        importlib.reload(mod)
_LOADED = True


class ObjectPanel(bpy.types.Panel):
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


REGISTER_CLASSES = [ObjectPanel]

import bpy

from ..lib import pkginfo

if "_LOADED" in locals():
    import importlib

    for mod in (pkginfo,):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()


class ThePreferencesPanel(bpy.types.AddonPreferences):
    bl_idname = package_name
    preferences_checkbox_property: bpy.props.BoolProperty(
        name="Turn on checkbox in preferences panel",
        description="If this checkbox is checked, then it is checked",
        default=False
    )

    def draw(self, context) -> None:
        layout = self.layout
        layout.prop(self, 'preferences_checkbox_property')


REGISTER_CLASSES = [ThePreferencesPanel]

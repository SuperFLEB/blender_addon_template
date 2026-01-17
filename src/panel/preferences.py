import bpy
from ..lib import pkginfo
from ..lib import f8

f8.reload(pkginfo) # Reload any imports here

package_name = pkginfo.package_name()


class PreferencesPanel(bpy.types.AddonPreferences):
    bl_idname = package_name
    preferences_checkbox_property: bpy.props.BoolProperty(
        name="Turn on checkbox in preferences panel",
        description="If this checkbox is checked, then it is checked",
        default=False
    )

    def draw(self, context) -> None:
        layout = self.layout
        layout.prop(self, 'preferences_checkbox_property')


REGISTER_CLASSES = [PreferencesPanel]

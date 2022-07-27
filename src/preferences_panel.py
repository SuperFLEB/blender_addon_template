import bpy

package_name = __package__


class ThePreferencesPanel(bpy.types.AddonPreferences):
    bl_idname = package_name
    some_property: bpy.props.BoolProperty(
        name="Turn on checkbox in preferences panel",
        description="If this checkbox is checked, then it is checked",
        default=False
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'some_property')

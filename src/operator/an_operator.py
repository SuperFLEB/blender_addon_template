import bpy
from typing import Set
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator
from ..lib import f8
from ..lib import pkginfo
from ..lib import util

f8.reload(pkginfo, util) # Reload any imports here

package_name = pkginfo.package_name()


def generate_enum_items(self, context) -> list[tuple[str, str, str]]:
    result = []
    for sign in "+-":
        for axis in "XYZ":
            result.append((f"{sign}{axis}", f"Align {sign}{axis}", f"Align something on the {sign}{axis} axis"))
    return result


class UNTITLED_BLENDER_ADDON_OT_AnOperator(Operator):
    """Description goes here"""
    bl_idname = "untitled_blender_addon.an_operator"
    bl_label = "An Operator"
    bl_options = {'REGISTER', 'UNDO'}

    an_int_prop: IntProperty(name="Pick a number", description="Pick a number, any number", default=0)
    a_simple_enum: EnumProperty(name="Axis", items=[
        ("VALUE_X", "X", "Axis X"),
        ("VALUE_Y", "Y", "Axis Y"),
        ("VALUE_Z", "Z", "Axis Z"),

    ], default="VALUE_X")
    a_complicated_enum: EnumProperty(name="Letterpeople", items=[
        # Entries with an empty value ("") are column headers and cannot be selected.
        # Value,    Name,     Description,          Icon,     Index
        ("", "Letters", "This is a header for the Letters column"),
        ("ITEM_A", "Item A", "Static enum item A", "EVENT_A", 0),
        ("ITEM_B", "Item B", "Static enum item B", "EVENT_B", 1),
        ("ITEM_C", "Item C", "Static enum item C", "EVENT_B", 1),
        ("", "People", "This is a header for the People column"),
        ("ALICE", "Alice", "A person named Alice"),
        ("BOB", "Bob", "A person named Bob"),
        ("CHARLIE", "Charlie", "A person named Charlie"),
    ], default="ITEM_A")
    a_generated_enum: EnumProperty(name="Alignment", items=generate_enum_items)
    is_red: BoolProperty(name="R", default=False)
    is_green: BoolProperty(name="G", default=False)
    is_blue: BoolProperty(name="B", default=False)

    @classmethod
    def poll(cls, context) -> bool:
        # Tooltip if the poll returns False
        cls.poll_message_set('You are not yet ready to harness the power of An Operator')
        return True

    @classmethod
    def can_show(cls, context) -> bool:
        # Similar to the poll() method, but manually implemented to completely omit the menu item from showing.
        return True

    def draw(self, context) -> None:
        self.layout.prop(self, "an_int_prop")

        axis_row = self.layout.row(align=True)
        axis_row.label(text="Axis:")
        axis_row.prop(self, "a_simple_enum", expand=True)

        rgb_row = self.layout.row(align=True)
        rgb_row.label(text="Channels:")
        rgb_row.prop(self, "is_red", toggle=1)
        rgb_row.prop(self, "is_green", toggle=1)
        rgb_row.prop(self, "is_blue", toggle=1)

        self.layout.prop(self, "a_complicated_enum")
        self.layout.prop(self, "a_generated_enum")
        self.layout.label(text="Click OK to continue", icon="LIGHT")

    def invoke(self, context, event) -> Set[str]:
        util.reset_operator_defaults(self, [
            "an_int_prop",
            "a_simple_enum",
            "a_complicated_enum"
        ])

        # You probably want to omit the invoke_props_dialog in operators that work in the 3D view,
        # as the Redo panel will handle configuration. Instead, either omit the invoke method entirely,
        # or return like:
        # return execute(self, context)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context) -> Set[str]:
        prefs = context.preferences.addons[package_name].preferences

        def message(menu, _) -> None:
            checked = prefs["preferences_checkbox_property"] if "preferences_checkbox_property" in prefs else False
            was_not_was = "was" if checked else "was not"
            your_number = self.an_int_prop
            menu.layout.label(text="It worked!", icon="SOLO_ON")
            menu.layout.label(text=f"Your number was {your_number}. Was I right?", icon="QUESTION")
            menu.layout.label(text=f"The checkbox in the Preferences panel {was_not_was} checked",
                              icon="CHECKMARK" if checked else "X")

        bpy.context.window_manager.popup_menu(message, title="Untitled Blender Addon")
        return {'FINISHED'}


REGISTER_CLASSES = [UNTITLED_BLENDER_ADDON_OT_AnOperator]

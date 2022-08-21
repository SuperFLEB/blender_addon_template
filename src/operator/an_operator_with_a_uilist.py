import bpy
from typing import Set
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator, PropertyGroup, UIList
from ..lib import pkginfo
from ..lib import util

if "_LOADED" in locals():
    import importlib

    for mod in (pkginfo, util,):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()


class APropertyGroup(PropertyGroup):
    hex: StringProperty(
        name="Hex",
        description="Hexidecimal form of the number",
    )
    integer: IntProperty(
        name="Integer",
        description="Integer form of the number",
    )
    is_even: BoolProperty(
        name="Even",
        description="Is the number even?"
    )


class AUIList(UIList):
    """A UIList to display some numbers"""
    bl_label = "Numbers"
    bl_idname = "CUSTOM_UL_numbers"

    def filter_items(self, context, data, propname):
        # the_properties is from data.<propname>, which has the list items as a list of APropertyGroup instances
        the_properties = getattr(data, propname)

        # To sort, return a list (of the same length) with the indices of the incoming list ordered as they should
        # be sorted. E.g., to sort a list backwards, the sorting list should be [5,4,3,2,1]
        resorted = sorted(
            # Generate a list of dicts with (unsorted) index and value, because we store the unsorted index
            # and use the value to finesse the sort.
            [{"was_idx": idx, "value": value} for idx, value in enumerate(the_properties)],
            # Finesse the sorting here if you want, or remove this if you don't need to
            key=lambda item: item["value"].integer
        )

        new_order = [item["was_idx"] for item in resorted]

        # To filter, make a list of ints that either have self.bitflag_filter_item (to show)
        # or ~self.bitflag_filter_item (to hide)
        filter_flags = [
            # Filter so we see only items less than 100 and odds over 100
            self.bitflag_filter_item if (item.integer < 100 or (item.integer % 2)) else ~self.bitflag_filter_item
            for item in the_properties
        ]

        # If you do not need to filter or sort, return an empty list in place of the filter or sort list, since that
        # accomplishes the same thing but is cheaper.
        # If you need to do neither, just omit the filter_items function.
        #
        # e.g.,
        # return [], new_order
        # return filter_flags, []
        return filter_flags, new_order

    def draw_item(self, context, layout, data, item, iocon, active_data, active_propname, index) -> None:
        layout.label(icon="OUTLINER_OB_LIGHT" if item.is_even else "LIGHT")
        layout.label(text=str(item.integer))
        layout.label(text=item.hex)


class AnOperatorWithUIList(Operator):
    """Description goes here"""
    bl_idname = "untitled_blender_addon.an_operator_with_uilist"
    bl_label = "UIList Operator"
    bl_options = {'REGISTER', 'UNDO'}

    uilist_items: CollectionProperty(type=APropertyGroup)
    active_uilist_index: IntProperty(name="Selected", default=0)

    @classmethod
    def poll(cls, context) -> bool:
        return True

    def draw(self, context) -> None:
        self.layout.label(
            text=f"You picked {self.uilist_items[self.active_uilist_index].integer} ({self.uilist_items[self.active_uilist_index].hex})")
        self.layout.template_list("CUSTOM_UL_numbers", "a_list_of_numbers", self, "uilist_items", self,
                                  "active_uilist_index")

    def invoke(self, context, event) -> Set[str]:
        util.reset_operator_defaults(self, [
            "active_uilist_index"
        ])

        # Populate the uilist_items collection to populate the UIList. This can be done here or in execute, as needed.
        # With the filtering (see above), even numbers over 100 will not be shown.
        numbers_to_pick = list(range(1, 21)) + list(range(100, 121))
        self.uilist_items.clear()
        for num in numbers_to_pick:
            uilist_item: APropertyGroup = self.uilist_items.add()
            uilist_item.hex = hex(num)
            uilist_item.integer = num
            uilist_item.is_even = bool((num + 1) % 2)

        # You probably want to omit this in operators that work in the 3D view, as the Redo panel will handle
        # configuration. Instead, either omit the invoke method entirely, or return like:
        # return execute(self, context)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context) -> Set[str]:
        prefs = context.preferences.addons[package_name].preferences

        def message(menu, _) -> None:
            menu.layout.label(
                text=f"You picked {self.uilist_items[self.active_uilist_index].integer} ({self.uilist_items[self.active_uilist_index].hex})")

        bpy.context.window_manager.popup_menu(message, title="Untitled Blender Addon")
        return {'FINISHED'}


REGISTER_CLASSES = [APropertyGroup, AUIList, AnOperatorWithUIList]

import bpy

_BL_CATEGORY = "Untitled Addon"

class MainPanel(bpy.types.Panel):
    bl_idname = "UNTITLEDADDON_PT_main"
    bl_label = "Untitled Addon"
    # bl_region_type = "WINDOW"|"HEADER"|"CHANNELS"|"TEMPORARY"|"UI"|"TOOLS"|"TOOL_PROPS"|"PREVIEW"|"HUD"|
    #                  "NAVIGATION_BAR"|"EXECUTE"|"FOOTER"|"TOOL_HEADER"|"XR"
    bl_region_type = "UI"
    # bl_space_type = "CLIP_EDITOR"|"CONSOLE"|"DOPESHEET_EDITOR"|"EMPTY"|"FILE_BROWSER"|"GRAPH_EDITOR"|"IMAGE_EDITOR"|
    #                 "INFO"|"NLA_EDITOR"|"NODE_EDITOR"|"OUTLINER"|"PREFERENCES"|"PROPERTIES"|"SEQUENCE_EDITOR"|
    #                 "SPREADSHEET"|"STATUSBAR"|"TEXT_EDITOR"|"TOPBAR"|"VIEW_3D"
    bl_space_type = "VIEW_3D"
    bl_category = _BL_CATEGORY
    # bl_options = set()|{'DEFAULT_CLOSED'}
    bl_options = set()

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        self.layout.label(text="Panel Title")

    def draw(self, context):
        self.layout.operator("object.untitled_blender_addon")



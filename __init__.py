import bpy

from .TileMarkers import TileMarkers
from .dynamic_property import *
from .config import config_panels
from .config import PropertyDataTypes
from . import tile_marker_type_list_operators as list_operators

bl_info = {
    "name": "Tile marker",
    "author": "Crenantious",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Add > Mesh > Tile markers",
    "description": "Generates tile markers on an object based on the generated grease pencil.",
    "warning": "",
    "doc_url": "",
}

addon_keymaps = []

def register():
    register_property(bpy.types.Object, "is_tile_marker", False)

    bpy.utils.register_class(PropertyDataTypes.TileMarkerType)
    bpy.utils.register_class(PropertyDataTypes.DataGroup)
    bpy.utils.register_class(TileMarkers)

    from .config import data
    from .config import tile_marker_types
    data.init()
    tile_marker_types.init()

    bpy.utils.register_class(list_operators.AddMarkerType)
    bpy.utils.register_class(list_operators.RemoveMarkerType)
    bpy.utils.register_class(list_operators.MoveMarkerTypeUp)
    bpy.utils.register_class(list_operators.MoveMarkerTypeDown)

    bpy.utils.register_class(config_panels.ConfigPanel)
    bpy.utils.register_class(config_panels.Material_UI_LIST)
    bpy.utils.register_class(config_panels.MaterialsPanel)
    bpy.utils.register_class(config_panels.EditTileMarkerTypePanel)

    bpy.types.VIEW3D_MT_object.append(menu_func)

    register_keymaps()

def register_keymaps():
    keymaps = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    items = keymaps.keymap_items.new(TileMarkers.bl_idname, 'F9', 'PRESS', ctrl=True, shift=True)
    items.active = True
    addon_keymaps.append((keymaps, items))


def unregister():
    bpy.utils.unregister_class(config_panels.MaterialsPanel)
    bpy.utils.unregister_class(config_panels.Material_UI_LIST)
    bpy.utils.unregister_class(config_panels.EditTileMarkerTypePanel)
    bpy.utils.unregister_class(config_panels.ConfigPanel)

    bpy.utils.unregister_class(list_operators.AddMarkerType)
    bpy.utils.unregister_class(list_operators.RemoveMarkerType)
    bpy.utils.unregister_class(list_operators.MoveMarkerTypeUp)
    bpy.utils.unregister_class(list_operators.MoveMarkerTypeDown)

    bpy.utils.unregister_class(TileMarkers)
    bpy.utils.unregister_class(PropertyDataTypes.DataGroup)
    bpy.utils.unregister_class(PropertyDataTypes.TileMarkerType)

    bpy.types.VIEW3D_MT_object.remove(menu_func)
    unregister_keymaps()


def unregister_keymaps():
    for keymaps, items in addon_keymaps:
        keymaps.keymap_items.remove(items)
    addon_keymaps.clear()


def menu_func(self, context):
    self.layout.operator(TileMarkers.bl_idname, text="Add tile markers", icon='PLUGIN')
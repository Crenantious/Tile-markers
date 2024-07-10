import bpy
from . import marker_type

class Index:
    @property
    def value(self):
        return bpy.context.scene.marker_types_index

    def set(self, value):
        bpy.context.scene.marker_types_index = value

    @property
    def max(self):
        return max(0, len(bpy.context.scene.marker_types) - 1)

    def increment(self):
        self.set(self.value + 1)
        self.clamp()

    def decrement(self):
        self.set(self.value - 1)
        self.clamp()

    def set_to_begining(self):
        self.set(0)

    def set_to_end(self):
        self.set(self.max)

    def clamp(self):
        self.set(max(0, min(self.value, self.max)))

class TileMarkerTypes:
    def __init__(self):
        self.__index = Index()

    @property
    def types(self):
        return bpy.context.scene.marker_types
    
    @property
    def index(self):
        return self.__index
    
    def get_active_item(self):
        if len(self.types) == 0:
            return None
        
        return self.types[self.index.value]

    def add(self):
        self.types.add()
    
    def remove(self, index):
        self.types.remove(index)
        self.index.clamp()
    
    def remove_current(self):
        self.types.remove(self.index.value)
        self.index.clamp()
    
    def move_up(self):
        if self.index.value <= 0:
            return
        
        self.types.move(self.index.value, self.index.value - 1)
        self.index.decrement()

    def move_down(self):
        if self.index.value >= self.index.max:
            return
        
        self.types.move(self.index.value, self.index.value + 1)
        self.index.increment()
    
marker_types = TileMarkerTypes()

def init():
    bpy.types.Scene.marker_types = bpy.props.CollectionProperty(type = marker_type.MarkerType)
    bpy.types.Scene.marker_types_index = bpy.props.IntProperty(name = "Index for marker_types", default = 0)
import bpy

properties = {}


def __get(obj, name):
    return properties[(obj, name)]
    #return getattr(obj, name).value


def __set(obj, name, value):
    properties[(obj, name)] = value
    #getattr(obj, name).value = value


def register_property(obj, name, default_value=None):
    setattr(obj, name, property(fget=lambda self: __get(self, name),
                                fset=lambda self, value: __set(self, name, value)))
    if hasattr(obj, name):
        if type(getattr(obj, name)) == Property:
            raise Exception
        return

   #
    setattr(obj, name, property(fget=lambda self: __get(self, name),
                                fset=lambda self, value: __set(self, name, value)))


class Property:
    def __init__(self, value):
        self.value = value

    def get(self, name):
        return self.properties[name]

    def set(self, name, value):
        self.properties[name] = value

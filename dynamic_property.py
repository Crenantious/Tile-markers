def __get(obj, name):
    return getattr(obj, "__" + name)[0]

def __set(obj, name, value):
    getattr(obj, "__" + name)[0] = value

def register_property(obj, name, default_value=None):
    setattr(obj, name, property(fget=lambda self: __get(self, name),
                                fset=lambda self, value: __set(self, name, value)))
    setattr(obj, "__" + name, [None])
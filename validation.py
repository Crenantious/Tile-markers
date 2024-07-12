import bpy
from . import gpencil as gp

class Validators:
    def __init__(self):
        self.validators = []

    def add(self, validator):
        self.validators.append(validator)

    def validate(self):
        errors = set()
        for validator in self.validators:
            result = validator.func(*validator.args)

            if result is None:
                continue

            errors.add(result)

            if validator.callback is not None:
                validator.callback()

            if validator.pass_through:
                continue

        return errors

class Validator:
    def __init__(self, func, pass_through = False, callback = None, *args):
        self.func = func
        self.pass_through = pass_through
        self.callback = callback
        self.args = args

    def set_args(self, *args):
        self.args = args

def validate_area(context):
    if context.area.type != 'VIEW_3D':
        #self.report({'WARNING'}, "View3D not found, cannot run operator")
        return 'CANCELLED'  

active_operator = None
def validate_active_operator():
    global active_operator
    if active_operator is not None:
        active_operator.finish()
        active_operator = None

def validate_gpencil():
    if gp.gpencil.object_exists() and gp.gpencil.is_object_active() and gp.gpencil.is_mode_correct():
        bpy.ops.object.mode_set(mode='OBJECT')
        return 'FINISHED'

def validate_modal_event(event):
    obj = bpy.context.view_layer.objects.active
    return event.type == 'MOUSEMOVE' and obj is not None and obj == gp.gpencil.object
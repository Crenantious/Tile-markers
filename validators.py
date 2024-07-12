import bpy
from . import gpencil as gp
from .validation import *

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
    if gp.gpencil.does_object_exist() is False:
        gp.gpencil.create()

    if gp.gpencil.is_object_active() and gp.gpencil.is_mode_correct():
        bpy.ops.object.mode_set(mode='OBJECT')
        return 'FINISHED'

    gp.gpencil.set_object_active()
    bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

def validate_modal_event(self, event):
    if self.is_finished:
        return 'FINISHED'
    
    if event.type == 'MOUSEMOVE' and gp.gpencil.is_object_active() and gp.gpencil.is_object_active():
        return

    return 'PASS_THROUGH'
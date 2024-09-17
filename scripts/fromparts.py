import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
import bpy
import sys
import math


def cleanup():
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)
    bpy.data.lights.remove(bpy.data.lights.get("Light"))
    bpy.data.cameras.remove(bpy.data.cameras.get("Camera"))


def setup_scale():
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit = "MILLIMETERS"


def setup_viewport():
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            space = area.spaces.active
            if space.type == "VIEW_3D":
                space.shading.type = "RENDERED"

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.device = 'GPU'


def setup_camera():
    camera_data = bpy.data.cameras.new(name="my-camera-data")
    camera = bpy.data.objects.new(name="my-camera", object_data=camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = 0, 0, 260
    camera.rotation_euler = 0, 0, 0
    camera.scale[0] = 1
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            area.spaces[0].region_3d.view_perspective = "CAMERA"
            break


def setup_light():
    light_data = bpy.data.lights.new(name="my-light-data", type='SPOT')
    light = bpy.data.objects.new(name="my-light", object_data=light_data)
    bpy.context.scene.collection.objects.link(light)

    light.data.energy = 1e9
    light.data.spot_size = math.pi/4
    light.data.shadow_soft_size = 5
    light.location[0] = 0
    light.location[1] = 0
    light.location[2] = 5
    light.rotation_euler[0] = math.pi
    light.rotation_euler[1] = 0
    light.rotation_euler[2] = 0
    light.scale[0] = 1


def add_rod():
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\6mm rod 400mm long v1.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    
    return obj

def create_rods():
    obj = add_rod()
    obj.location = [-30, -30, 0]
    obj = add_rod()
    obj.location = [30, -30, 0]
    obj = add_rod()
    obj.location = [30, 30, 0]
    obj = add_rod()
    obj.location = [-30, 30, 0]
    

def create_illuminator():
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage base v5.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = math.pi, 0, 0
    obj.scale = 10, 10, 10
    
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\LED illuminator heat sink assembly v5.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    

def create_collector():
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage v54.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 20
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage with hole ACL2520U-0DG6-A-Step v11.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 20
    glass = obj.data.materials["Glass_(Clear)"]
    glass.node_tree.nodes["Principled BSDF"].inputs[
        "Transmission Weight"
    ].default_value = 1.0
    glass.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.0   


def create_condenser():
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage v54.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 60
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage moving piece with hole for condenser v16.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 60
    glass = obj.data.materials["Glass_(Clear).001"]
    glass.node_tree.nodes["Principled BSDF"].inputs[
        "Transmission Weight"
    ].default_value = 1.0
    glass.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.0   
    
    

def create_sample():
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental Microscope slide holder v3.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 80
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Microscope slide with stage micrometer v4.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = math.pi, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 80+8
    glass = obj.data.materials["Glass_(Clear).002"]
    glass.node_tree.nodes["Principled BSDF"].inputs[
        "Transmission Weight"
    ].default_value = 1.0
    glass.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.0   
    
def create_objective():
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage v54.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 100
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage moving piece with hole for LB1092 v2.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 100
   
    glass = obj.data.materials["Opaque(244,242,245)"]
    glass.node_tree.nodes["Principled BSDF"].inputs[
        "Transmission Weight"
    ].default_value = 1.0
    glass.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.0   
    

def create_camera():
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage v54.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 260
    
    bpy.ops.wm.obj_import(filepath=r"Z:\src\blender_lens_experiment\objects\Experimental XY stage with hole for camera v9.obj")
    obj = bpy.context.view_layer.objects.active
    obj.rotation_euler = 0, 0, 0
    obj.scale = 10, 10, 10
    obj.location = 0, 0, 260
   
def main():
    cleanup()

    setup_scale()
    setup_viewport()
    setup_camera()
    setup_light()
    
    create_rods()
    create_illuminator()
    create_collector()
    create_condenser()
    create_sample()
    create_objective()
    create_camera()

if __name__ == "__main__":
    main()

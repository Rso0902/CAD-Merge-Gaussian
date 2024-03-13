import blenderproc as bproc
import os
import argparse
import numpy as np
import bpy
import bmesh

# parser = argparse.ArgumentParser()
# parser.add_argument("front", help="Path to the 3D front file")
# parser.add_argument("future_folder", help="Path to the 3D Future Model folder.")
# parser.add_argument("front_3D_texture_path", help="Path to the 3D FRONT texture folder.")
# parser.add_argument("output_dir", help="Path to where the data should be saved")
# args = parser.parse_args()

# if not os.path.exists(args.front) or not os.path.exists(args.future_folder):
#     raise Exception("One of the two folders does not exist!")

bproc.init()
mapping_file = bproc.utility.resolve_resource(os.path.join("front_3D", "3D_front_mapping.csv"))
mapping = bproc.utility.LabelIdMapping.from_csv(mapping_file)

# set the light bounces
bproc.renderer.set_light_bounces(diffuse_bounces=200, glossy_bounces=200, max_bounces=200,
                                  transmission_bounces=200, transparent_max_bounces=200)

# load the front 3D objects
file_path = '3D-Front/data/3D-FRONT/0a9f5311-49e1-414c-ba7b-b42a171459a3.json'
loaded_objects = bproc.loader.load_front3d(
    json_path=file_path,
    future_model_path='3D-Front/data/3D-FUTURE-model',
    front_3D_texture_path='3D-Front/data/3D-FRONT-texture',
    label_mapping=mapping
)

loaded_objects[0].join_with_other_objects(loaded_objects[1:])
scene_MeshObject = loaded_objects[0]

scene_mesh = scene_MeshObject.get_mesh()
obj = bpy.data.objects.new(name="Cube", object_data=scene_mesh)
# bpy.context.scene.collection.objects.link(obj)

bpy.context.view_layer.objects.active = obj
# bpy.ops.wm.save_as_mainfile(filepath="/home/rso/codes/CAD_Merge_NeRF/3D-Front/1.blend")
bpy.ops.export_scene.fbx(file_path='/home/rso/codes/CAD_Merge_NeRF/3D-Front/' + file_path.split('/')[-1].split('.')[0] + '.fbx',
                         use_selection = True)

#Meshobj有这个方法join_with_other_objects
import blenderproc as bproc
import os
import argparse
import numpy as np
import bpy
import bmesh

parser = argparse.ArgumentParser()
parser.add_argument("--front", help="Path to the 3D front file", type=str, required=False, default='./data/3D-FRONT/0a482eb4-e8fa-4b44-90d0-3623e0a60c71.json')
parser.add_argument("--future_folder", help="Path to the 3D Future Model folder.", type=str, required=False, default='./data/3D-FUTURE-model')
parser.add_argument("--front_3D_texture_path", help="Path to the 3D FRONT texture folder.", type=str, required=False, default='./data/3D-FRONT-texture')
parser.add_argument("--output_dir", help="Path to where the data should be saved", type=str, required=False, default='./create_dataset/scene_model')
args = parser.parse_args()

if not os.path.exists(args.front) or not os.path.exists(args.future_folder):    
    raise Exception("One of the two folders does not exist!")

bproc.init()
mapping_file = bproc.utility.resolve_resource(os.path.join("front_3D", "3D_front_mapping.csv"))
mapping = bproc.utility.LabelIdMapping.from_csv(mapping_file)

# set the light bounces
bproc.renderer.set_light_bounces(diffuse_bounces=200, glossy_bounces=200, max_bounces=200,
                                  transmission_bounces=200, transparent_max_bounces=200)

# load the front 3D objects
loaded_objects = bproc.loader.load_front3d(
    json_path=args.front,
    future_model_path=args.future_folder,
    front_3D_texture_path=args.front_3D_texture_path,
    label_mapping=mapping
)

def check_name(name):
    for category_name in ["ceiling"]:
        if category_name not in name.lower():
            return True
    return False


# filter some objects from the loaded objects, which are later used in calculating an interesting score
special_objects = [obj for obj in loaded_objects if check_name(obj.get_name())]

special_objects[0].join_with_other_objects(special_objects[1:])
scene_MeshObject = special_objects[0]

scene_mesh = scene_MeshObject.get_mesh()
obj = bpy.data.objects.new(name=args.front.split('/')[-1].split('.')[0], object_data=scene_mesh)
bpy.context.scene.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bpy.ops.export_scene.fbx(filepath=os.path.join(args.output_dir, args.front.split('/')[-1].split('.')[0] + '_rich_without_ceiling.fbx'),
                         use_selection = True)

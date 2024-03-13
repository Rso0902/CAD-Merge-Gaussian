import blenderproc as bproc
import os
import argparse
import numpy as np
import bpy
import bmesh
import random
from PIL import Image
import json

parser = argparse.ArgumentParser()
parser.add_argument("--front", help="Path to the 3D front file", type=str, required=False, default='./data/3D-FRONT/0a482eb4-e8fa-4b44-90d0-3623e0a60c71.json')
parser.add_argument("--future_folder", help="Path to the 3D Future Model folder.", type=str, required=False, default='./data/3D-FUTURE-model')
parser.add_argument("--front_3D_texture_path", help="Path to the 3D FRONT texture folder.", type=str, required=False, default='./data/3D-FRONT-texture')
parser.add_argument("--camera_matrix_path", help="Path to the camera matrix folder.", type=str, required=False, default='./create_dataset/camera_matrixs')
parser.add_argument("--intermediate_file", help="Path to where the intermediate data should be saved", type=str, required=False, default='./create_dataset/intermediate_file')
parser.add_argument("--dataset_dir", help="Path to where the dataset should be saved", type=str, required=False, default='./create_dataset/dataset')
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
# load the front 3D objects
loaded_objects = bproc.loader.load_front3d(
    json_path=args.front,
    future_model_path=args.future_folder,
    front_3D_texture_path=args.front_3D_texture_path,
    label_mapping=mapping
)


# Init sampler for sampling locations inside the loaded front3D house
point_sampler = bproc.sampler.Front3DPointInRoomSampler(loaded_objects)

# Init bvh tree containing all mesh objects
bvh_tree = bproc.object.create_bvh_tree_multi_objects([o for o in loaded_objects if isinstance(o, bproc.types.MeshObject)])

#TODO：得到对应场景的相机位姿
camera_matrix_file = os.path.join(args.camera_matrix_path, args.front.split('/')[-1].split('.')[0]+'.txt')
assert os.path.exists(camera_matrix_file), camera_matrix_file + 'not exists'
with open(camera_matrix_file, 'r') as file:
    lines = file.readlines()
    
matrix_data = []
for line in lines[1:]:
    row_data = line.strip().split(' ')
    row_data = [float(value) for value in row_data]
    matrix_data.append(row_data)

camera_params = [float(value) for value in lines[0].strip().split(' ')[:-1]] + lines[0].strip().split(' ')[-1:]
cam2world_matrixes = []
for i in range(0, len(matrix_data), 4):
    cam2world_matrixes.append(matrix_data[i:i+4])
    cam2world_matrix = np.array(matrix_data[i:i+4])
    bproc.camera.add_camera_pose(cam2world_matrix)
    #TODO:相机参数也是需要脚步读取的
    # bproc.camera.set_intrinsics_from_blender_params(lens=came, image_width=1200, image_height=680, clip_start=0.1, clip_end=1000,
    #                                                 pixel_aspect_x=1, pixel_aspect_y=1, shift_x=0, shift_y=0, lens_unit='MILLIMETERS')
    bproc.camera.set_intrinsics_from_blender_params(lens=camera_params[0], image_width=int(camera_params[1]), image_height=int(camera_params[2]), clip_start=camera_params[3], clip_end=camera_params[4],
                                                    pixel_aspect_x=camera_params[5], pixel_aspect_y=camera_params[6], shift_x=camera_params[7], shift_y=camera_params[8], lens_unit=camera_params[10])


bproc.renderer.enable_normals_output()
data = bproc.renderer.render()
#输出的png图像是需要在场景名称的路径下
inter_path = os.path.join(args.intermediate_file, args.front.split('/')[-1].split('.')[0])
if not os.path.exists(inter_path):
    os.mkdir(inter_path)
# write the data to a .hdf5 container
bproc.writer.write_gif_animation(inter_path, data, save_path=inter_path)
#TODO:保存为NeRF数据集的格式
dataset_path = os.path.join(args.dataset_dir, args.front.split('/')[-1].split('.')[0])
if not os.path.exists(dataset_path):
    os.mkdir(dataset_path)
    
#首先创建包含所有下标的列表
indices = [i for i in range(len(cam2world_matrixes))]
random.shuffle(indices)
#对列表按照2:1:1分成，train、test、val
data_partition = {"train": indices[:-2], 
                  "test": indices[-2: -1], 
                  "val": indices[-1: ]}
print(data_partition)

def save_dataset(data_type: str, indices: list, cam2world_matrixes: list, camera_angle_x, dataset_path: str, inter_dir: str):
    data_path = os.path.join(dataset_path, data_type)
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    data_infos = {"camera_angle_x": camera_angle_x,
                 "frames": []}
    for ind in indices:
        info = {"file_path": "./"+data_type+"/"+str(ind)+"_colors",
                "rotation": 0,
                "transform_matrix": cam2world_matrixes[ind]}
        data_infos['frames'].append(info)
        
        image_normal = Image.open(os.path.join(inter_dir, str(ind)+"_normals.png"))
        image_color = Image.open(os.path.join(inter_dir, str(ind)+"_colors.png"))
        image_color_array = np.array(image_color)
        image_normal_array = np.array(image_normal)
        background_value = [127, 127, 127, 255]
        background_mask = np.all(image_normal_array==background_value, axis=-1).astype(np.uint8) *255
        image_color_array[background_mask==255] = [0, 0, 0, 0]
        image = Image.fromarray(image_color_array)
        image.save(os.path.join(data_path , str(ind)+"_colors.png"))
    json_path = os.path.join(dataset_path, "transforms_" + data_type + ".json")
    with open(json_path, "w") as json_file:
        json.dump(data_infos, json_file)

for data_type, indices in data_partition.items():
    save_dataset(data_type, indices, cam2world_matrixes, camera_params[9], dataset_path, inter_path)


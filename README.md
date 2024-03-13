### CREATE DATASET
1. get into the folder of 3D-Front
2. then make the scene model
```python
blenderproc run ./create_dataset/export_fbx.py {path_to_front} {path_to_future_folder} {path_to_front_3D_texture_path} {scene_output_dir}
```
3. place the camera fllow_path in the blender, and run the script `./create_dataset/export_camera_matrix.py` in blender.
4. export the .ply file from the mesh model in blender
5. then make the NeRF likes dataset
```python
python export_multiview.py {Path_of_the_3D_front_file} {Path to the 3D Future Model foler} {Path to the 3D front texture folder} {Path to the camera matrix folder} {Path to where the intermidiate  data should be save} {Path to where the dataset should be save}
```
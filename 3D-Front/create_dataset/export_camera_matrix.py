import bpy

#Export pose for keyframe animation of blender's active camera
# !!!!! Make sure you have set active camera!!!
#The pose is a 4*4 matrix
#If what you need is the coordinate system of OpenCV, then after using this script, you still need to invert the y and z of the 4*4 pose rotation part.

# Set export file name
export_file = "/home/rso/codes/CAD_Merge_NeRF/3D-Front/create_dataset/camera_matrixs/0a482eb4-e8fa-4b44-90d0-3623e0a60c71.txt"
# Make sure camera is selected
camera = bpy.context.scene.camera
if camera is not None and camera.type == 'CAMERA':

    # Get the start and end frames of the animation
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end

    # save current frame
    current_frame = bpy.context.scene.frame_current

    # Prepare a list for storing camera transformation matrices
    camera_transforms = []
    camera_params = []
    scene = bpy.data.scenes[0]
    camera_params += [camera.data.lens, scene.render.resolution_x, scene.render.resolution_y,
                      camera.data.clip_start, camera.data.clip_end, scene.render.pixel_aspect_x,
                      scene.render.pixel_aspect_y, camera.data.shift_x, camera.data.shift_y, camera.data.angle_x, camera.data.lens_unit]
    # iterate over all frames on the track
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()
        bpy.context.evaluated_depsgraph_get().update() 
        matrix = camera.matrix_world.copy()
        camera_transforms.append({"frame": frame, "matrix": matrix})

    # restore the original current frame
    bpy.context.scene.frame_set(current_frame)

    # Export to TXT file
    with open(export_file, 'w') as txtfile:
        txtfile.write(" ".join([str(value) for value in camera_params]) + "\n")
        for transform in camera_transforms:
            for row in transform["matrix"]:
                txtfile.write(" ".join([str(value) for value in row]) + "\n")

    print(f"Camera transforms exported to {export_file}")
else:
    print("No camera selected or active object is not a camera.")
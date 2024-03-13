from plyfile import PlyData, PlyElement
import numpy as np

def fetchPly(path):
    plydata = PlyData.read(path)
    vertices = plydata['vertex']
    positions = np.vstack([vertices['x'], vertices['y'], vertices['z']]).T
    return vertices, positions

if __name__ == "__main__":
    path = "../3D-Front/create_dataset/scene_model/untitled.ply"
    vertices, positions = fetchPly(path)
    print(positions.shape)
import argparse
import os
from cv2 import normalize

import numpy as np
import open3d as o3d

def parse_args():
    parser = argparse.ArgumentParser('sampler')
    parser.add_argument('--input_dir', type=str, default='data/admorph', help='input dir')
    parser.add_argument('--num_points', type=int, default=10000, help='number of points')
    parser.add_argument('--normalize', type=bool, default=True, help='normalize')
    return parser.parse_args()

def pc_normalize(pc):
    centroid = np.mean(pc, axis=0)
    pc = pc - centroid
    m = np.max(np.sqrt(np.sum(pc**2, axis=1)))
    pc = pc / m
    return pc

def sample_point_cloud(mesh, n=10000, normalize=True):
    '''
    sample point cloud
    '''
    points =  mesh.sample_points_uniformly(number_of_points=n)
    coords = points.points
    if normalize:
        coords = pc_normalize(points.points)
    return np.hstack((coords, points.normals))

def convert_stl(root, class_name, n, normalize):
    '''
    convert stl file to point cloud
    '''
    dir_path = os.path.join(root, class_name)
    files = os.listdir(dir_path)
    count = 0
    for file in files:
        if file.endswith('.stl'):
            count += 1
            mesh = o3d.io.read_triangle_mesh(os.path.join(dir_path, file))
            points = sample_point_cloud(mesh, n, normalize)
            
            # ouput_name: class_name_XXXX.txt (XXXX: is count)
            output_path = os.path.join(dir_path, class_name + '_' + str(count).zfill(4) + '.txt')
            np.savetxt(output_path, points, delimiter=',', fmt='%.6f')

            # remove original stl file
            os.remove(os.path.join(dir_path, file))



if __name__== "__main__":
    args = parse_args()
    root = args.input_dir
    normalize = args.normalize
    num_points = args.num_points
    catfile = os.path.join(root, 'admorph_shape_names.txt')
    cat = [line.rstrip() for line in open(catfile)]

    for c in cat:
        convert_stl(root, c, n=num_points, normalize=normalize)
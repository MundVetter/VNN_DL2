import argparse
import os
import open3d as o3d

def parse_args():
    parser = argparse.ArgumentParser('sampler')
    parse.add_argument('--input_dir', type=str, default='data/admorph', help='input dir')

def sample_point_cloud(mesh, n=10000):
    '''
    sample point cloud
    '''
    points = mesh.sample_points_uniform(n)
    return points

if __name__== "__main__":
    # args = parse_args()
    # main(args)
    path = 'data/admorph/Acanthodii indet/acanthodian-01_1.stl'
    mesh = o3d.io.read_triangle_mesh(path)
    points = sample_point_cloud(mesh)
    o3d.visualization.draw_geometries([mesh, points])
    o3d.io.write_point_cloud('data/admorph/Acanthodii indet/acanthodian-01_1_sample.ply', points)
    print('done')
"""
Author: Congyue Deng
Contact: congyue@stanford.edu
Date: April 2021
"""
from data_utils.ModelNetDataLoader import ModelNetDataLoader
import argparse
import numpy as np
import os
import torch
import logging
from tqdm import tqdm
import sys
import importlib
from pytorch3d.transforms import RotateAxisAngle, Rotate, random_rotations
from models.utils.activ_util import ACTIV_MAP, get_activ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = BASE_DIR
sys.path.append(os.path.join(ROOT_DIR, 'models'))


def parse_args():
    '''PARAMETERS'''
    parser = argparse.ArgumentParser('PointNet')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size in training [default: 32]')
    parser.add_argument('--model', default='vn_dgcnn_cls', help='Model name [default: vn_dgcnn_cls]',
                        choices = ['pointnet_cls', 'vn_pointnet_cls', 'dgcnn_cls', 'vn_dgcnn_cls'])
    parser.add_argument('--gpu', type=str, default='0', help='Specify gpu device [default: 0]')
    parser.add_argument('--num_point', type=int, default=1024, help='Point Number [default: 1024]')
    parser.add_argument('--log_dir', type=str, default='vn_dgcnn/aligned', help='Experiment root [default: vn_dgcnn/aligned]')
    parser.add_argument('--normal', action='store_true', default=False, help='Whether to use normal information [default: False]')
    parser.add_argument('--num_votes', type=int, default=3, help='Aggregate classification scores with voting [default: 3]')
    parser.add_argument('--rot', type=str, default='aligned', help='Rotation augmentation to input data [default: aligned]',
                        choices=['aligned', 'z', 'so3'])
    parser.add_argument('--pooling', type=str, default='mean', help='VNN only: pooling method [default: mean]',
                        choices=['mean', 'max'])
    parser.add_argument('--n_knn', default=20, type=int, help='Number of nearest neighbors to use, not applicable to PointNet [default: 20]')
    parser.add_argument('--activ', type=str, default=None, help='Activation function [default: author LeakyReLU]',
                        choices=ACTIV_MAP.keys())
    parser.add_argument('--magnitude_activation', action='store_true', default=False, help='Whether to use authors magnitude activation [default: False]')
    return parser.parse_args()

def test(model, loader, num_class=40, vote_num=1):
    mean_correct = []
    class_acc = np.zeros((num_class,3))
    for j, data in tqdm(enumerate(loader), total=len(loader)):
        points, target = data
        
        trot = None
        if args.rot == 'z':
            trot = RotateAxisAngle(angle=torch.rand(points.shape[0])*360, axis="Z", degrees=True)
        elif args.rot == 'so3':
            trot = Rotate(R=random_rotations(points.shape[0]))
        if trot is not None:
            points[:, :, :3] = trot.transform_points(points[:, :, :3])
            if args.normal:
                points[:, :, 3:] = trot.transform_points(points[:, :, 3:])
        
        target = target[:, 0]
        points = points.transpose(2, 1)
        points, target = points.cuda(), target.cuda()
        classifier = model.eval()
        vote_pool = torch.zeros(target.size()[0],num_class).cuda()
        for _ in range(vote_num):
            pred, _ = classifier(points)
            vote_pool += pred
        pred = vote_pool/vote_num
        pred_choice = pred.data.max(1)[1]
        for cat in np.unique(target.cpu()):
            classacc = pred_choice[target==cat].eq(target[target==cat].long().data).cpu().sum()
            class_acc[cat,0]+= classacc.item()/float(points[target==cat].size()[0])
            class_acc[cat,1]+=1
        correct = pred_choice.eq(target.long().data).cpu().sum()
        mean_correct.append(correct.item()/float(points.size()[0]))
    class_acc[:,2] =  class_acc[:,0]/ class_acc[:,1]
    class_acc = np.mean(class_acc[:,2])
    instance_acc = np.mean(mean_correct)
    return instance_acc, class_acc


def main(args):
    def log_string(str):
        logger.info(str)
        print(str)

    '''HYPER PARAMETER'''
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu

    '''CREATE DIR'''
    experiment_dir = 'log/cls/' + args.log_dir

    '''LOG'''
    args = parse_args()
    logger = logging.getLogger("Model")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('%s/eval.txt' % experiment_dir)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    log_string('PARAMETER ...')
    log_string(args)

    # Retrieve activation function from name.
    args.activ = get_activ(args.activ, args.magnitude_activation)

    '''DATA LOADING'''
    log_string('Load dataset ...')
    DATA_PATH = 'data/modelnet40_normal_resampled/'
    TEST_DATASET = ModelNetDataLoader(root=DATA_PATH, npoint=args.num_point, split='test', normal_channel=args.normal)
    testDataLoader = torch.utils.data.DataLoader(TEST_DATASET, batch_size=args.batch_size, shuffle=False, num_workers=4)

    '''MODEL LOADING'''
    num_class = 40
    MODEL = importlib.import_module(args.model)
    
    classifier = MODEL.get_model(args, num_class, normal_channel=args.normal).cuda()

    checkpoint = torch.load(str(experiment_dir) + '/checkpoints/best_model.pth')
    classifier.load_state_dict(checkpoint['model_state_dict'])

    with torch.no_grad():
        instance_acc, class_acc = test(classifier.eval(), testDataLoader, vote_num=args.num_votes)
        log_string('Test Instance Accuracy: %f, Class Accuracy: %f' % (instance_acc, class_acc))



if __name__ == '__main__':
    args = parse_args()
    main(args)

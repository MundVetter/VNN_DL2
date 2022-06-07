# Vector Neurons++: Extending Neural Dimensionality and Generalizing Activation Functions for Vector Neuron Networks

This code base is forked from VN-PointNet <a href="https://github.com/FlyingGiraffe/vnn-pc/" target="_blank">Deng et al.</a>.
We introduce the addition of arbitrary activation and inclusion of normals in the VN-layers, specifically for PointNet.
For DGCNN we refer to https://github.com/CSteigstra/vnn-pc which is based on its correct implementation from https://github.com/FlyingGiraffe/vnn-pc .

## Overview
`vnn++` is the author's implementation of Vector Neuron Networks with PointNet and DGCNN backbones. The current version only supports PointNet for Modelnet40 classification.

## Environment
```
conda env create -f dl2_gpu.yml
conda activate dl2
# or 
source activate dl2
```

## Data Preparation

+ Classification: Download [ModelNet40](https://shapenet.cs.stanford.edu/media/modelnet40_normal_resampled.zip) and save in `data/modelnet40_normal_resampled/`.

## Usage

### Classification on ModelNet40
Training
```
# Author's (Deng et al.) LeakyReLU
python train_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --optimizer Adam --rot z
python train_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --optimizer Adam --rot z --normal
# Ours
python train_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --optimizer Adam --rot z --activ leaky_relu
python train_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --optimizer Adam --rot z --activ leaky_relu --normal
```

Evaluation
```
# Author's (Deng et al.) LeakyReLU
python test_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --rot so3
python test_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --rot so3 --normal
# Ours
python test_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --rot so3 --activ leaky_relu
python test_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --rot so3 --activ leaky_relu --normal
```

## Citation
In the works. Refer to our github for now. ^.^

## License
MIT License

## Acknowledgement
The structure of this codebase is borrowed from this pytorch implementataion of [PointNet/PointNet++](https://github.com/yanx27/Pointnet_Pointnet2_pytorch) and [DGCNN](https://github.com/WangYueFt/dgcnn) as well as [this implementation](https://github.com/AnTao97/dgcnn.pytorch).

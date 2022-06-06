# Vector Neurons ++: VNN++: Extending Neural Dimensionality and Generalizing Activation Functions for Vector Neuron Networks

This code base is forked from VN-PointNet <a href="https://github.com/FlyingGiraffe/vnn-pc/ target="_blank">Deng et al.</a>.
We introduce a general framework built on top of what we call Vector Neurons for creating SO(3) equivariant neural networks. Extending neurons from single scalars to 3D vectors, our vector neurons transport SO(3) actions to latent spaces and provide a framework for building equivariance in common neural operations including linear layers, non-linearities, pooling, and normalization.

## Overview
`vnn++` is the author's implementation of Vector Neuron Networks with PointNet and DGCNN backbones. The current version only supports input data without normals.

## Data Preparation

+ Classification: Download [ModelNet40](https://shapenet.cs.stanford.edu/media/modelnet40_normal_resampled.zip) and save in `data/modelnet40_normal_resampled/`.
+ Part Segmentation: Download [ShapeNet](https://shapenet.cs.stanford.edu/media/shapenetcore_partanno_segmentation_benchmark_v0_normal.zip)  and save in `data/shapenetcore_partanno_segmentation_benchmark_v0_normal/`.

## Usage

### Classification on ModelNet40
Training
```
python train_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --optimizer Adam --rot z --activ sigmoid
python train_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --optimizer Adam --rot z --activ sigmoid --normal
```

Evaluation
```
python test_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --rot z --activ sigmoid
python train_cls.py --log_dir LOG_DIR --model vn_pointnet_cls --rot so3 --activ sigmoid --normal
```

## Citation
In the works. Refer to our github for now. ^.^

## License
MIT License

## Acknowledgement
The structure of this codebase is borrowed from this pytorch implementataion of [PointNet/PointNet++](https://github.com/yanx27/Pointnet_Pointnet2_pytorch) and [DGCNN](https://github.com/WangYueFt/dgcnn) as well as [this implementation](https://github.com/AnTao97/dgcnn.pytorch).

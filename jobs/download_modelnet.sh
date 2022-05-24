#!/bin/bash

wget --no-check-certificate https://shapenet.cs.stanford.edu/media/modelnet40_normal_resampled.zip -O modelnet.zip
unzip -q modelnet.zip -d data/
rm modelnet.zip

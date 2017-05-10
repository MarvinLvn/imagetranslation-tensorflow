# Image translation by CycleGAN and pix2pix in Tensorflow

This is my ongoing tensorflow implementation for unpaired image-to-image translation ([Zhu et al., 2017](https://arxiv.org/pdf/1703.10593.pdf)). 

Latest results can be found here, [comparing](docs/run_1.md) paired and unpaired image-to-image translation.
 
Image-to-image translation learns a mapping from input images to output images, like these examples from the original papers: 

#### CycleGAN: [[Project]](https://junyanz.github.io/CycleGAN/) [[Paper]](https://arxiv.org/pdf/1703.10593.pdf) [[Torch]](https://github.com/junyanz/CycleGAN)
<img src="https://junyanz.github.io/CycleGAN/images/teaser_high_res.jpg" width="900"/>

#### Pix2pix:  [[Project]](https://phillipi.github.io/pix2pix/) [[Paper]](https://arxiv.org/pdf/1611.07004v1.pdf) [[Torch]](https://github.com/phillipi/pix2pix)

<img src="https://phillipi.github.io/pix2pix/images/teaser_v3.png" width="900px"/>

## Prerequisites
- Linux or OSX.
- Python 2 or Python 3.
- CPU or NVIDIA GPU + CUDA CuDNN.

## Requirements
Tensorflow 1.0

## Preferred
- Anaconda Python distribution
- PyCharm

## Getting Started
Clone this repository
```sh
git clone https://github.com/tbullmann/imagetranslation-tensorflow.git
cd imagetranslation-tensorflow
```
Install Tensorflow, e.g. [with Anaconda](https://www.tensorflow.org/install/install_mac#installing_with_anaconda)

Create directories or symlink
```sh
mkdir datasets  # or symlink; for datasets
mkdir temp  # or symlink; for checkpoints, test results
```
Download the CMP Facades dataset (generated from http://cmp.felk.cvut.cz/~tylecr1/facade/)
```sh
python tools/download-dataset.py facades datasets
```
Train the model (this may take 1-8 hours depending on GPU, on CPU you will be waiting for a bit)
```sh
python translate.py \
  --model pix2pix \
  --mode train \
  --output_dir temp/facades_train \
  --max_epochs 200 \
  --input_dir datasets/facades/train \
  --which_direction BtoA
```

Test the model
```sh
python translate.py \
  --model pix2pix \
  --mode test \
  --output_dir temp/facades_test \
  --input_dir datasets/facades/val \
  --checkpoint temp/facades_train
```
The test run will output an HTML file at `temp/facades_test/index.html` that shows input/output/target image sets.

For training of the CycleGAN use ```--model CycleGAN``` instead of ```--model pix2pix```. 
Both models use u-net as generator by default but can use faststyle-net when specified by ```--generator faststyle```.

You can look at the loss and computation graph for [pix2pix](docs/run_1_images/Graph_Pix2Pix.png) and [CycleGAN](docs/run_1_images/Graph_CycleGAN.png) using tensorboard:

```sh
tensorboard --logdir=temp/facades_train
```  

If you wish to write in-progress pictures as the network is training, use ```--display_freq 50```. This will update ```temp/facades_train/index.html``` every 50 steps with the current training inputs and outputs.

## TODO

### Finish CycleGAN implementation according to publication Hu et al., 2017
Major issues
- add instance normalization ([Ulyanov D et al., 2016](https://arxiv.org/abs/1607.08022))
- add image buffer that stores the previous image (to update discriminators using a history of 50 generated images)
Minor issues
- flexible learning rate for the Adams solver
- add one-direction test mode for CycleGAN
- add identity loss

### Import and export
- images with arbitrary height width and color channels (input/target)
- add mask for unlabeled regions (by restricting losses to labeled regions)
- add more preprocessing options for augmentation
- move lab_colorization(split input image into brightness and color)

### Testing
- test transfer learning from Pix2Pix2 to CycleGAN
- fully test CPU mode and multi-GPU mode
- add different generators 

### Other
- resize-convolution on top of deconvolution for better upsampling ([Odena et al., 2016](http://distill.pub/2016/deconv-checkerboard/))
- add dropout layers to faststyle net

## Done
- test CycleGAN with u-net generator and log loss and compare with pix2pix: [OK](docs/run_1.md) 
- test CycleGAN with faststyle-net generator and log loss: [OK](docs/run_1.md) 
- square loss and several options for loss function for generator (maximising discriminator loss, ...)
- refactor summary and export of images to work for all models: Pix2Pix, CycleGAN, Pix2Pix2
- two batches delivering unpaired images for CycleGAN
- import of images from different subdirectories

## Acknowledgement

This repository is based on [this](https://github.com/affinelayer/pix2pix-tensorflow) Tensorflow implementation of the paired image-to-image translation ([Isola et al., 2016](https://arxiv.org/pdf/1611.07004v1.pdf)) 

## Citation

If you use this code for your research, please cite the papers this code is based on:

```tex
@article{pix2pix2016,
  title={Image-to-Image Translation with Conditional Adversarial Networks},
  author={Isola, Phillip and Zhu, Jun-Yan and Zhou, Tinghui and Efros, Alexei A},
  journal={arxiv},
  year={2016}
}

@article{CycleGAN2017,
  title={Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networkss},
  author={Zhu, Jun-Yan and Park, Taesung and Isola, Phillip and Efros, Alexei A},
  journal={arXiv preprint arXiv:1703.10593},
  year={2017}
}

@inproceedings{johnson2016perceptual,
  title={Perceptual losses for real-time style transfer and super-resolution},
  author={Johnson, Justin and Alahi, Alexandre and Fei-Fei, Li},
  booktitle={European Conference on Computer Vision},
  pages={694--711},
  year={2016},
  organization={Springer}
}
```
Practical 1 bis: HourGlass vs U-net
=========================================

## Goals

- implement HourGlass network
- implement U-net
- compare both methods
- optionally, you can test generative models on this basis: auto-encoder, VAE

## Evaluation
The practical will be evaluated in groups of two.
It is expected that you write a report with the plots / results of the 
different experiments. The code must be submitted with the report.

A good report :
* briefly details the experiment setting 
* illustrates the results (with screenshots, tables)
* briefly discusses the outcome of the experiment

```
Reports are due on December 1st 2023
```

## Getting started



### Dataset
1. Data is contained from the tictoc dance sequences.
   - **dataset** : The dataset contains the images and the masks stored on
     Ensimag machines in folder `/matieres/5MMVORF/04-dataset`, referred
     throughout as `dataset` folder below for simplicity. 
     
   - [`train.py`](train.py) is the file containing the main training code.

### References

The original articles where some of the architectures were described.

[1] U-Net: Convolutional Networks for Biomedical Image Segmentation ;
Olaf Ronneberger, Philipp Fischer, Thomas Brox ; 2015

## Part 1 : Examine the code

A first naive attempt to segment is provided through the SimpleConv architecture, which runs the image through a series of convolutions.
A first stack of convolutions encodes increasingly more features, and a second decodes progressively less features, until it predicts just one value per pixel, which corresponds to our segmentation per pixel.

1. Run the training code and predict.
2. Does it converge easily?
3. What happens if you put more encoding, decoding layers?

## Part 1 : Hourglass convolutional neural network

Implement the following Hourglass convolutional neural network, starting with a copy of the SimpleConv class. In the following diagram, you see what we want to achieve: instead of layering maive convolutions, we want to create a bottleneck, where the number of features is reduced and creates a 'latent space' encoding the abstract space of people segmentations. To this goal, you must add pooling layers in the network encoder part to progressively reduce the size of the feature map. Reciprocally, in the decoder loop, you must upscale the features such that the size of the output image coincides with the input size (same number of upconvolutions). Consult the documentation of [ConvTranspose2D](https://pytorch.org/docs/stable/generated/torch.nn.ConvTranspose2d.html) in PyTorch.

![alt the hourglass][hourglass]

[hourglass]: hourglass_scheme.png "HourGlass scheme"

**Questions**

1. What do you observe with convergence? Make several training attempts if necessary.
2. Vary the number of features and depth encoding layers. For each of these attempts, can you predict what is the size of the bottleneck map? Verify your predictions by printing its actual size. Comment on how the performance varies with the depth of the network / size of the bottleneck.

## Part 2 : U-net convolutional neural network
U-Net was invented to address precision problems of the original hourglass network. 
Implement the following U-net convolutional neural network, with 3 encoding and 3 decoding layers proposed, starting with a copy of your Hourglass.

![alt the unet][unet]

[unet]: unet_scheme.png "U-Net scheme"

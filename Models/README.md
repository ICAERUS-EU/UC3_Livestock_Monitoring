# Cow Detection Model

This repository contains code for a cow detection model using PyTorch and YOLO. <br>

## Requirements

- **GPU**: The model requires a GPU to train efficiently. Please ensure that you have access to a GPU before proceeding. <br>
- **PyTorch Library**: Refer to the PyTorch website to install the appropriate version based on your operating system. You can find the installation instructions here: <https://pytorch.org/> <br>
- **YOLO Library**: You can install the YOLO library by running `pip install ultralytics`.
- **yaml file**: Give the access directory to the dataset.

## Dataset

The dataset used for training this model consists of images collected from two outdoor cattle farms in France using a UAV. The flights were conducted at an altitude of 100 meters in nadir position. Images and their corresponding labeling files are available on the Zenodo repository [ICAERUS HE Project](https://zenodo.org/records/10245396).

## Data Preparation

The original resolution of the input images is 640x640 pixels. However, if desired, you may choose to resize the images prior to making predictions using alternative packages such as SAHI. Instructions and tutorials for using SAHI can be found on [SAHI github repository](https://github.com/obss/sahi) or in [ultralytics guide](https://docs.ultralytics.com/fr/guides/sahi-tiled-inference/).

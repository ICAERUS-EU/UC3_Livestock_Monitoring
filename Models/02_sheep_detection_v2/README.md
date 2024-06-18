# Sheep Detection Model v2

This repository contains code for a sheep detection model using YOLO v8. <br>

## Requirements

- **GPU**: The model requires a GPU to train efficiently. Please ensure that you have access to a GPU before proceeding. <br>
- **PyTorch Library**: Refer to the PyTorch website to install the appropriate version based on your operating system. You can find the installation instructions here: <https://pytorch.org/> <br>
- **YOLO Library**: You can install the YOLO library by running `pip install ultralytics`.
- **yaml file**: Give the access directory to the dataset.

## Dataset
This model was built using two roboflow universe dataset and annotated videos from our sheep dataset. All of them contained aerial photos of sheeps.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br>
 Dataset 3: Images extracted from videos obtained by drone in Carmejane farm. Videos and annotations available [here](https://zenodo.org/communities/icaerus_he/records?q=&l=list&p=1&s=10&sort=newest). 
 

All images from both are organized in train/validation/test directories:

|  | Train | Validation | Test |
| --- | :---: | :---: | :---: | 
| Dataset 1 | 3 609| 350 | 174 |
| Dataset 2 | 777 | 78 | 39 |
| Dataset 3 | 225 | 297 | 117 |
|Total | 4 611 | 725 | 330 |

## Model parameters

- pre-trained model: yolov8m.pt
- batch: 8
- optimizer: auto
- lr: 0.01
- momentum: 0.937

## Results

Precision: 0.94 <br>
Recall: 0.75

https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/assets/99217487/14c859e3-67df-4f5b-87ae-a7211ad3bd4b





# Sheep Detection Model v1

This repository contains code for a sheep detection model using YOLO v8. <br>

## Requirements

- **GPU**: The model requires a GPU to train efficiently. Please ensure that you have access to a GPU before proceeding. <br>
- **PyTorch Library**: Refer to the PyTorch website to install the appropriate version based on your operating system. You can find the installation instructions here: <https://pytorch.org/> <br>
- **YOLO Library**: You can install the YOLO library by running `pip install ultralytics`.
- **yaml file**: Give the access directory to the dataset.

## Dataset
This model was built using two roboflow universe dataset. Both contained aerial photos of sheeps 

<!-- 
référence /citation git ?
 -->
 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1)

All images from both are organized in train/validation/test:

|  | Train | Validation | Test |
| --- | :---: | :---: | :---: | 
| Dataset 1 | 3 609| 350 | 174 |
| Dataset 2 | 777 | 78 | 39 |
|Total | 4 386 | 428 | 213 |

## Model parameters

- pre-trained model: yolov8m.pt
- batch: 8
- optimizer: auto
- lr: 0.01
- momentum: 0.937

## Results

- recall = 0.76
- precision = 0.93

https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/assets/99217487/0bbd56ab-905b-473e-91db-b5fb0aa479ef



<!--


-->




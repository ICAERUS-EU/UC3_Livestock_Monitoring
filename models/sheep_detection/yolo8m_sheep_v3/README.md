# 🐏 Sheep Detection Model v3

This repository contains code for a sheep detection model using YOLOv8m. <br>

## 📄 Dataset
This model was built using five roboflow universe datasets and a personal dataset that will soon be available in Zenodo. All of them contained aerial photos of sheeps.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br>
 Dataset 3 : [Dusksheepuav](https://universe.roboflow.com/lars-wuethrich/dusksheepuav) <br>
 Dataset 4 : [Rough Terrain Sheep UAV](https://universe.roboflow.com/lars-wuethrich/roughterrainsheepuav) <br>
 Dataset 5 : [Snow Sheep UAV](https://universe.roboflow.com/lars-wuethrich/snowsheepuav) <br>
 Dataset 6 : [Personal Dataset, available on Zenodo - link to come]

All images from both are organized in train/validation directories:

|  | Train | Validation |
| :---: | :---: | :---: |
| Dataset 1 | 3 609| 350 | 
| Dataset 2 | 777 | 78 |
| Dataset 3 | 411 | 31 |
| Dataset 4 | 414 | 0 |
| Dataset 5 | 582 | 41 |
| Dataset 6 | 80 | 0 |
|Total | 5 873 | 500 |

## Model parameters

- pre-trained model: yolov8m.pt
- batch: 4
- optimizer: auto
- lr: 0.01
- momentum: 0.937

## Results

Model was evaluated on a test directory containing 639 images of [walking sheeps](https://zenodo.org/records/12094356).

| Images | Instances | Precision | Recall | mAP50 | mAP50-95
| :---: | :---: | :---: | :---: | :---: | :---: |
| 639  | 14365 | 0.941 | 0.901 | 0.966 |   0.654 |


# 🐏 Sheep Detection Model v3

This repository contains code for a sheep detection model using YOLOv8m. <br>

## 📄 Dataset
This model was built using five roboflow universe datasets and a personal dataset available in Zenodo. All of them contained aerial photos of sheeps.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br>
 Dataset 3 : [Dusksheepuav](https://universe.roboflow.com/lars-wuethrich/dusksheepuav) <br>
 Dataset 4 : [Rough Terrain Sheep UAV](https://universe.roboflow.com/lars-wuethrich/roughterrainsheepuav) <br>
 Dataset 5 : [Snow Sheep UAV](https://universe.roboflow.com/lars-wuethrich/snowsheepuav) <br>
 Dataset 6 :  [Drone images and their annotations of sheep in various conditions (for computer vision purpose)](https://zenodo.org/records/18889623)

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

The model was evaluated on a test dataset consisting of 428 images of sheep taken from a nadir view. These images and their labels are available in this [Zenodo repository](https://zenodo.org/records/18889623), in the Nadir_only folder.

| Images | Instances | Precision | Recall | mAP50 | mAP50-95
| :---: | :---: | :---: | :---: | :---: | :---: |
| 428  |  2906 |  0.956 |  0.956 |  0.988  | 0.919 | 


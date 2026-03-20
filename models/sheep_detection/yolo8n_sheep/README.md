# 🐏 Sheep Detection Model 

This repository contains code for a sheep detection model using YOLOv8n. <br>

**This is so far our gold standard sheep detection model.**

## 📄 Dataset
This model was built using five roboflow universe datasets and a personal dataset available in Zenodo. All of them contained aerial photos of sheeps.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br>
 Dataset 3 : [Dusksheepuav](https://universe.roboflow.com/lars-wuethrich/dusksheepuav) <br>
 Dataset 4 : [Rough Terrain Sheep UAV](https://universe.roboflow.com/lars-wuethrich/roughterrainsheepuav) <br>
 Dataset 5 : [Snow Sheep UAV](https://universe.roboflow.com/lars-wuethrich/snowsheepuav) <br>
 Dataset 6 : [Drone images and their annotations of sheep in various conditions (for computer vision purpose)](https://zenodo.org/records/18889623)

All images from both are organized in train/validation directories:

|  | Train | Validation |
| Dataset 1 | 3 609| 350 | 
| Dataset 2 | 777 | 78 |
| Dataset 3 | 411 | 31 |
| Dataset 4 | 414 | 0 |
| Dataset 5 | 582 | 41 |
| Dataset 6 | 265 | 46 |
|Total | 6 058 | 546 |

## Model parameters

- pre-trained model: yolov8n.pt
 
- batch: 16
- optimizer: SGD
- lr0: 0.1
- lrf: 0.03
- momentum: 0.937

## Results

The model was evaluated on a test dataset consisting of 428 images of sheep taken from a nadir view. These images and their labels are available in this [Zenodo repository](https://zenodo.org/records/18889623), in the Nadir_only folder.

| Images | Instances | Precision | Recall | mAP50 | mAP50-95
| :---: | :---: | :---: | :---: | :---: | :---: |
| 428   | 2906  |  0.966 | 0.964  | 0.99  | 0.88 |


# 🐏 Sheep Detection Model v1

This repository contains code for a sheep detection model using YOLO v8. <br>

## 📄 Dataset
This model was built using two roboflow universe dataset. Both contained aerial photos of sheeps 

<!-- 
référence /citation git ?
 -->
 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1)

All images from both are organized in train/validation/test:

|  | Train | Validation |
| --- | :---: | :---: |
| Dataset 1 | 3 609| 350 | 
| Dataset 2 | 777 | 78 |
|Total | 4 386 | 428 |

## Model parameters

- pre-trained model: yolov8m.pt
- batch: 8
- optimizer: auto
- lr: 0.01
- momentum: 0.937

## Results

The model was evaluated on a test dataset consisting of 428 images of sheep taken from a nadir view. These images and their labels are available in this [Zenodo repository](https://zenodo.org/records/18889623), in the Nadir_only folder.

| Images | Instances | Precision | Recall | mAP50 | mAP50-95
| :---: | :---: | :---: | :---: | :---: | :---: |
| 428  | 2906  | 0.93  | 0.832  |  0.899  | 0.698 |

https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/assets/99217487/0bbd56ab-905b-473e-91db-b5fb0aa479ef



<!--


-->




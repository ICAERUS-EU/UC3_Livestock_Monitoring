# 🐏 Sheep Detection Model using YOLO11n

This repository contains code for a sheep detection model using YOLOv11n. <br>

## 📄 Dataset
This model was built using two roboflow universe dataset. All of them contained aerial photos of sheeps.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br> 
 

All images from both are organized in train/validation directories:

|  | Train | Validation |
| --- | :---: | :---: |
| Dataset 1 | 3 609| 350 |
| Dataset 2 | 777 | 78 |
|Total | 4 611 | 725 |


## Model parameters

- pre-trained model: yolov11n.pt
- batch: 8
- optimizer: auto
- lr: 0.01
- momentum: 0.937

## Results

|  | precision | recall | mAP50 | mAP50-95 | fitness
| --- | :---: | :---: | :---: | :---: | :---: 
| **yolo11n_sheep** | 0.893652 | 0.763918 | 0.862653 | 0.577639 | 0.606140


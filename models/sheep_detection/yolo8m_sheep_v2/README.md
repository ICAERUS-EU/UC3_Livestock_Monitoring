# 🐏 Sheep Detection Model v2

This repository contains code for a sheep detection model using YOLO v8. <br>

## 📄 Dataset
This model was built using two roboflow universe dataset and annotated videos from our sheep dataset. All of them contained aerial photos of sheeps.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br>
 Dataset 3: Images extracted from videos obtained by drone in Carmejane farm. Videos and annotations available [here](https://zenodo.org/communities/icaerus_he/records?q=&l=list&p=1&s=10&sort=newest). 
 

All images from both are organized in train/validation directories:

|  | Train | Validation |
| --- | :---: | :---: |
| Dataset 1 | 3 609| 350 |
| Dataset 2 | 777 | 78 |
| Dataset 3 | 225 | 297 | 
|Total | 4 611 | 725 |

## Model parameters

- pre-trained model: yolov8m.pt
- batch: 8
- optimizer: auto
- lr: 0.01
- momentum: 0.937

## Results

| precision | recall | mAP50 | mAP50-95 | fitness
| :---: | :---: | :---: | :---: | :---: 
| 0.920961 | 0.811414	| 0.902250 | 0.683201 | 0.705105


https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/assets/99217487/14c859e3-67df-4f5b-87ae-a7211ad3bd4b





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

The model was evaluated on a test dataset consisting of 428 images of sheep taken from a nadir view. These images and their labels are available in this [Zenodo repository](https://zenodo.org/records/18889623), in the Nadir_only folder.

| Images | Instances | Precision | Recall | mAP50 | mAP50-95
| :---: | :---: | :---: | :---: | :---: | :---: |
| 428  | 2906  | 0.896 |  0.846 | 0.938 | 0.723 |


https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/assets/99217487/14c859e3-67df-4f5b-87ae-a7211ad3bd4b




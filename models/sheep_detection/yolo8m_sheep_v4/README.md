# 🐏 Sheep Detection Model v4

This repository contains code for a sheep detection model using YOLOv8m. <br>

**This is so far our gold standard sheep detection model.**

## 📄 Dataset
This model was fine-tuned from the sheep detection model v3 using several images of dataset 1 and 2 and images of a new dataset recently annotated. This dataset contains images of sheeps of various sizes, various colors and in various background.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br>
 Dataset 6 : [Drone images and their annotations of sheep in various conditions (for computer vision purpose)](https://zenodo.org/records/18889623)

All images from both are organized in train/validation directories:

|  | Train | Validation |
| :---: | :---: | :---: |
| Dataset 1 | 66| 21 | 
| Dataset 2 | 24 | 2 |
| Dataset 6 | 185 | 46 |
|Total | 275 | 69 |

## Model parameters

Model was trained in two phases, one with a freeze of backbone during 10 epochs and the other with partial unfreeze for 80 epochs. Script used is available in [src/yolo_finetune_train.py ](../../../src/yolo_finetune_train.py)

- pre-trained model: yolov8m_sheep_v3.pt

phase A: 
- batch: 16
- optimizer: SGD
- lr0: 3e-4 
- lrf: 0.1 
- momentum: 0.937

phase B:
- batch: 16
- optimizer: SGD
- lr0: 1e-3
- lrf: 0.01
- momentum: 0.937

## Results

The model was evaluated on a test dataset consisting of 428 images of sheep taken from a nadir view. These images and their labels are available in this [Zenodo repository](https://zenodo.org/records/18889623), in the Nadir_only folder.

| Images | Instances | Precision | Recall | mAP50 | mAP50-95
| :---: | :---: | :---: | :---: | :---: | :---: |
| 428   | 2906  | 0.97 |  0.966 | 0.991 | 0.969 |


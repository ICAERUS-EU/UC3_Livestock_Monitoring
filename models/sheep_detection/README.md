# 🐏 Sheep Detection Models

This repository contains different models using YOLO to detect aerial sheep. <br>

## 💻 Requirements

- **GPU**: The models require a GPU to predict efficiently. Please ensure that you have access to a GPU before proceeding. <br>
- **PyTorch Library**: Refer to the PyTorch website to install the appropriate version based on your operating system. You can find the installation instructions here: <https://pytorch.org/> <br>
- **YOLO Library**: You can install the YOLO library by running `pip install ultralytics`.
- **yaml file**: Give the access directory to the dataset.
- **requirement file** : All requirements can be found in requirements.txt

## 📄 Dataset
These models were built using two roboflow universe dataset and  annotated videos from our sheep dataset. All of them contained aerial photos of sheeps.

 Dataset 1: [Aerial Sheep](https://universe.roboflow.com/riis/aerial-sheep/dataset/1) <br>
 Dataset 2: [Sheep Gen4](https://universe.roboflow.com/gbes/sheep-gen4/dataset/1) <br>
 Dataset 3: Images extracted from videos obtained by drone in Carmejane farm in France. Videos and annotations available [here](https://zenodo.org/communities/icaerus_he/records?q=&l=list&p=1&s=10&sort=newest). 
 

All images from both are organized in train/validation directories. Each detection model may have been trained and validated on different datasets, which will be detailed in the model directory.

|  | Train | Validation | 
| --- | :---: | :---: | 
| Dataset 1 | 3 609| 350 | 
| Dataset 2 | 777 | 78 |
| Dataset 3 | 225 | 297 | 
|Total | 4 611 | 725 | 

To compare the metrics of each model, **the same test directory** was used. This dataset contains various images of sheep of different colors and shapes. The images were taken by drone on various French farms. The annotated dataset will soon be added to Zenodo. 

## Results

Metrics of each model are shown below: 

|  | precision | recall | mAP50 | mAP50-95 | fitness
| --- | :---: | :---: | :---: | :---: | :---: 
| **yolo8m_sheep_v1** | 0.867717 | 0.754648 | 0.831524 | 0.622124 | 0.643064
| **yolo8m_sheep_v2** | 0.920961 | 0.811414	| 0.902250 | 0.683201 | 0.705105
| **yolo11n_sheep** | 0.893652 | 0.763918 | 0.862653 | 0.577639 | 0.606140
| **yolo11s_sheep** | 0.924347 | 0.799301 | 0.887569 | 0.640029 | 0.664783



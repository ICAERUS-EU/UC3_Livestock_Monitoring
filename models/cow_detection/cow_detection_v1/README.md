#  🐄 Cow Detection Model v1

This repository contains code for a cow detection model using PyTorch and YOLO. <br>

## 💻 Requirements

- **GPU**: The model requires a GPU to train efficiently. Please ensure that you have access to a GPU before proceeding. <br>
- **PyTorch Library**: Refer to the PyTorch website to install the appropriate version based on your operating system. You can find the installation instructions here: <https://pytorch.org/> <br>
- **YOLO Library**: You can install the YOLO library by running `pip install ultralytics`.
- **yaml file**: Give the access directory to the dataset.

## 📄 Dataset

The dataset used for training this model consists of images collected from three outdoor cattle farms in France using a UAV (Mavic 3 Enterprise or Mavic 3 Thermal). The flights were conducted at an altitude of 30, 60 or 100 meters in nadir position. Images and their corresponding labeling files are available on the Zenodo repository [ICAERUS HE Project](https://zenodo.org/records/10245396).

The following breeds with distinct body colors are present in the dataset:
- **White**: Charolaises in Jalogny farm
- **Spotted**: Prim'Holstein, Normandes in Mauron and Derval farms
- **Black/red**: Salers, along with some black Prim'Holstein in Mauron and Derval farms

Image size can be 4000x3000 or 5280x3956 depending on the drone used.

![Image collected in Mauron farm, 100m altitude, nadir position, cows with multiple body colors.](../../Docs/Images/mauron_example1.JPG)

## Data Preparation

All images with animals from the dataset were used (241 over 1148). Dataset was split into training, validation and test with a ratio of 70/20/10.


| Color body | White | Spotted | Red/Black |
| --- | :---: | :---: | :---: | 
| Number of images | 136  | 67 | 38 |
| Number of animals | 301 | 1435 | 357 | 

## Model parameters

- pre-trained model: yolov8m.pt
- batch: 8
- optimizer: auto
- lr: 0.01
- momentum: 0.937

## Results

Metrics: 
- Precision: 0.67
- Recall: 0.60
<br>

An example of cow detection in a image from test population:
![Detection of cows in the same image.](../../Docs/Images/mauron_example1_predict_v1.png)
# -*- coding: utf-8 -*-
'''
script for training yolo model on a custom dataset.
input : yaml file describing train and validation dataset localization.
'''


# import librairies
import torch
from ultralytics import YOLO

## test GPU
torch.cuda.current_device()

# give data localization via yaml file
yaml_directory = "directory/of/your/yaml/file"

# training model
model = YOLO("yolov8x.pt")

# training model
model.train(data = yaml_directory,
            epochs = 2000,
            patience = 30,
            batch = 8,
            device = 0,
            workers = 0,
            imgsz=640)

# model validation
model.val()
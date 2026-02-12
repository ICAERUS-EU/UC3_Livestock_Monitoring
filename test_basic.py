#%%
import os

#from ultralytics import YOLO
import src.video as video
import src.utils as utils

utils.split_train_val_test(path_dir="path/to/dataset",train_rate=0.8,val_rate=0.2)

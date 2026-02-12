'''
Functions to manipulate images and annotation files 
'''
import os
from tqdm import tqdm
import time
import random
import shutil

def write_prefix_files(dir_path: str, prefix: str) -> None:
    '''
    in a repository of frames or images, add a generic prefix  
    to all files contained.
    
    :param dir_path: Path to the files where names should be changed 
    :type dir_path: str
    :param prefix: Name to be add as prefix in all file names
    :type prefix: str
    '''
    list_path = os.listdir(dir_path)

    for file in tqdm(list_path, desc="In progress..."):
        new_name = f"{prefix}_{file}"
        os.rename(os.path.join(dir_path,file),os.path.join(dir_path,new_name))
        time.sleep(0.05)
    print(f'Success, all files renamed')

def convert_yolo_coco(bb_list:list, img_size:tuple) -> list:
    '''
    conversion from yolo annotation to coco.
    
    :param label_path: path to label file
    :param img_size: image size
    '''
    w, h = img_size
    boxes = []
    for boxe in bb_list:
            x_center = boxe[0]*w
            y_center = boxe[1]*h
            width = w*boxe[2]
            height = h*boxe[3]
            x1 = x_center - width/2
            y1 = y_center - height/2
            x2 = x_center + width/2
            y2 = y_center + height/2
            boxes.append([x1, y1, x2, y2])
    return boxes

def txt_extraction(dir_path: str, file_name: str) -> list:
    '''
    extract an annotation file with each detection into list of lists

    :param dir_path: folder containing labels folder with annotations
    :type dir_path: str
    :param file_name: file name of interest
    :type file_name: str
    :param output: list of lists containing annotations. 
    :type output: list
    '''
    annotated = []
    with open(os.path.join(dir_path,file_name), 'r') as f: 
        annotated += [list(map(float, line.split()[1:])) for line in f]
        return annotated

def all_txt_extraction(image_path:str) -> dict:
    '''
    extract each txt files componants of a directory into dictionary 

    :param dir_images: path to images folder associated with annotations files of interest
    :param output: dictionary with file names as key and contained annotations as a list of floats
    '''
    txt_annotation = {} 
    i = 0
    for root, dirs, files in os.walk(image_path):
        for elt in files:
                nom_seul = elt[:-4] # extract txt file name
                if elt.endswith("txt"):
                    annotated = []
                    with open(os.path.join(root, elt), encoding="utf-8") as f: 
                        annotated += [list(map(float, line.split()[1:])) for line in f] 
                    txt_annotation[nom_seul] = annotated
                    i+=1
    print(f'Extraction completed, \n Number of extracted files: {i}')
    return txt_annotation

def bbox_to_yoloformat(bounding_box: list, resolution: tuple):
    '''
    convert (xmin, ymin, xmax, ymax) bndbox coordinates to YOLO format (x_center, y_center, width, height)
    
    :param bounding_box: Description
    :type bounding_box: list
    :param resolution: Description
    :type resolution: tuple
    '''
    x_center = ((bounding_box[0] + bounding_box[2]) / 2.0) / resolution[0]
    y_center = ((bounding_box[1] + bounding_box[3]) / 2.0) / resolution[1]
    width = (bounding_box[2] - bounding_box[0]) / resolution[0]
    height = (bounding_box[3] - bounding_box[1]) / resolution[1]
    return x_center, y_center, width, height

def write_yolo_annotation_file(bb_list: list, output_file: str, resolution: tuple):
    """
    Save YOLO annotations in file

    :param bb_list: list of predicted detections obtained from prediction.extract_pred_bb [x0, y0, x1, y1, conf, cls]
    :type bb_list: list
    :param output_file: path to output file
    :type output_file: str
    :param resolution: width and height of image
    :type resolution: tuple
    """
    #TODO: hide function ?
    #TODO: add conf in file ?
    
    with open(output_file, 'w') as fichier:
        for element in bb_list:
            # convert bounding box format to yolo format
            x, y, w, h = bbox_to_yoloformat(element, resolution)
            label = int(element[5])
            # Write file with : label x y w h
            fichier.write(f"{label} {x:.4f} {y:.4f} {w:.4f} {h:.4f}\n")

def mkdir_image(path_dir, split_folder):
    if not os.path.isdir(os.path.join(path_dir,split_folder,'images')):
        os.makedirs(os.path.join(path_dir,split_folder,'images'))

def mkdir_label(path_dir, split_folder):
    if not os.path.isdir(os.path.join(path_dir,split_folder,'labels')):
        os.makedirs(os.path.join(path_dir,split_folder,'labels'))

def split_train_val_test(path_dir, train_rate, val_rate, ):
    '''
    split a path dir into 3 folder train/val/test according to rate and create labels/img folder inside
    
    :param path_dir: Description
    :param train_rate: Description
    :param val_rate: Description
    '''
    len_file = len([f for f in os.listdir(path_dir) 
    if f.lower().endswith('.jpg') and os.path.isfile(os.path.join(path_dir, f))])
     # separation des donnees

    n_train = 0
    n_val = 0
    n_test = 0

    list_jpg = []
    
    for file in os.listdir(path_dir):
        if file.endswith(('.JPG','.jpg')):
            n_train = int((len_file * train_rate)+0.5)
            n_val = int((len_file * val_rate) +0.5)
            n_test = len_file - (n_train+n_val)
            list_jpg.append(file)
    print('Images number in train: ', n_train)
    print('Images number in valid: ', n_val)
    print('Images number in test: ', n_test)

    # Data split
    image_random_train = random.sample(list_jpg, n_train)
    mkdir_image(path_dir,'train')
    mkdir_label(path_dir,'train')
    for file in image_random_train:
        file_label = file[:-3] + 'txt'
        shutil.move(os.path.join(path_dir,file), os.path.join(path_dir,'train','images'))
        # move label file if exists
        if os.path.isfile(os.path.join(path_dir,file_label)):
            shutil.move(os.path.join(path_dir,file_label), os.path.join(path_dir,'train', 'labels'))

    list_jpg = []
    for file in os.listdir(path_dir):
        if file.endswith(('.JPG','.jpg')):
            list_jpg.append(file)

    image_random_val = random.sample(list_jpg, n_val)
    mkdir_image(path_dir,'val')
    mkdir_label(path_dir,'val')

    for file in image_random_val:
        file_label = file[:-3] + 'txt'
        shutil.move(os.path.join(path_dir,file), os.path.join(path_dir,'val','images'))
        # move label file if exists
        if os.path.isfile(os.path.join(path_dir,file_label)):
            shutil.move(os.path.join(path_dir,file_label), os.path.join(path_dir,'val','labels'))

    # Update of remaining files
    list_jpg = []
    for file in os.listdir(path_dir):
        if file.endswith(('.JPG','.jpg')):
            list_jpg.append(file)
    mkdir_image(path_dir,'test')
    mkdir_label(path_dir,'test')

    # test folder
    for file in list_jpg:
        file_label = file[:-3] + 'txt'
        shutil.move(os.path.join(path_dir,file), os.path.join(path_dir,'val','images'))
        # move label file if exists
        if os.path.isfile(os.path.join(path_dir,file_label)):
            shutil.move(os.path.join(path_dir,file_label), 
                        os.path.join(path_dir,'val','labels'))

def find_txt_labels(img_path: str, txt_path:str) -> str:
    '''
    after selection of images, output = path to the corresponding label file
    '''
    for img in os.listdir(os.path.join(img_path,"images")):
        txt_name = img[:-3]+"txt"
        for root, dirs, files in os.walk(txt_path):
            if txt_name in files:
                '''if not os.path(os.path.join(img_path,"labels")):
                    mkdir_label(img_path,'labels')'''
                if not os.path.isfile(os.path.join(root,txt_name)):
                    print("none")
                    continue
                shutil.copy2(os.path.join(root,txt_name),
                            os.path.join(img_path,"labels",txt_name))
                print(img_path,"labels",txt_name)
    return os.path.join(root, txt_name)
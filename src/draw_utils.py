'''
functions to draw on images and movies
'''

from PIL import Image
from PIL import ImageDraw
import os
from random import randint

def show_annotation(dir_path:str, filename:str)-> None:
    '''
    Visualisation of bounding boxes on image
    :param dir_path: directory path
    :param filename = path to label file
    '''
    #TODO: add TypeError for im_data: must be ImageFile from PIL
        
    txt_path = os.path.join(dir_path,f'labels/{filename[:-4]}.txt')
    
    # open image file
    extensions = [".jpg", ".JPG", ".jpeg", ".JPEG"]
    
    img_path = None
    for ext in extensions:
        #print(os.path.join(dir_path, f"images/{filename}{ext}"))
        candidate = os.path.join(dir_path, f"images/{filename[:-4]}{ext}")
        if os.path.exists(candidate):
            img_path = candidate
            break

    if img_path is None:
        raise FileNotFoundError(f"{filename} None image file found with this extension.") 
        
    im_data = Image.open(img_path).copy()
    draw = ImageDraw.Draw(im_data)
    
    annotated_data = []
    with open(txt_path, 'r') as f: 
        annotated_data += [list(map(float, line.split()[1:])) for line in f]
    
    for liste in annotated_data:
        x_center_norm = liste[0]
        y_center_norm = liste[1]
        width_norm = liste[2]
        height_norm = liste[3]

        # Pixel conversion
        x_center = x_center_norm * im_data.size[0]
        y_center = y_center_norm * im_data.size[1]
        width = width_norm * im_data.size[0]
        height = height_norm * im_data.size[1]

        # Coordinates conversion
        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)
        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        animal = [x_min, y_min, x_max, y_max]
        draw.rectangle(animal, outline="red", width=5)

    im_data.show()   

def show_roi(im_path, roi, gt_roi, det_roi):
    '''
    show bounding boxes into ROI on image 

    :params im_path: path to image
    :params roi: ROI coordinates (rx1, ry1, rx2, ry2)
    :params gt_roi: Ground Truth coordinates
    :params det_roi: Predicted bndbox coordinates
    '''
    im = Image.open(im_path)
    # show image
    draw = ImageDraw.Draw(im)
    draw.rectangle(roi, fill=None, outline=None, width=2)
    for box in gt_roi:
        draw.rectangle(box[:4].tolist(), fill=None, outline="blue", width=2)
    for box in det_roi:
        draw.rectangle(box[:4].tolist(), fill=None, outline="red", width=2)
    im.show()

def random_colors(n):
    colors = []
    for _ in range(n):
        # Number generation between 0x000000 and 0xFFFFFF
        color = "#{:06x}".format(randint(0, 0xFFFFFF))
        colors.append(color)
    return colors
'''
Any function with connection with model detection and prediction
'''

import os
from tqdm import tqdm
import time

from PIL import Image
from PIL import ImageDraw

import numpy as np
import torch
from ultralytics.utils.metrics import ConfusionMatrix

from . import utils, draw_utils


#TODO: class bndbox

def extract_pred_bb(image_path:str, image: str, model_name : str, confidence: float = 0.5) -> list:
    '''
    Extraction of detected bounded boxes, confidence indice and class
    
    :param image_path: path to image file
    :type image_path: str
    :param image: image name
    :type image: str
    :param model_name: variable containing model charged 
    :type model_name: str
    :param confidence: confidence indice to attempt 
    :type confidence: float
    :return: List of bounding boxes
    :rtype: list
    '''
    bb_list = []
    results = model_name.predict(os.path.join(image_path, image), conf = confidence)
    result = results[0]
    # recup BB
    if not result:
            print(f'No predictions for {image} - pass')
            return None, None
            #raise Exception("result is empty")
    else:
        '''
        if detection found, extract bb and plot on image
        '''
        resolution = (result[0].orig_shape[1], result[0].orig_shape[0])
        bbox = result.boxes.data
        bbox_coord = bbox.data[:,:]
        for bounding_box in tqdm(bbox_coord, desc="In progress..."):
            bb_list.append(np.array(bounding_box))
        return bb_list, resolution

def show_predicted_bb(image_path:str, image: str, bb_list, output_path:str = None, saving_file : bool = True, show_image : bool = True) -> None:
        '''
        Run prediction on image and show bnbbox on image
        
        :param image_path: path to image
        :type image_path: str
        :param image: name of image
        :type image: str
        :param bb_list: List of predicted bounding boxes for the image
        :type: bb_list: list
        :param output_path: Give a output path to save annotated images
        :type output_path: str
        :param saving_file: If true, save image file with annotations
        :type saving_file: bool
        :param show_image: If true, show image file
        :type show_image: bool
        '''
        if output_path is None:
              output_path = image_path
        im = Image.open(os.path.join(image_path,image)).copy()
        draw = ImageDraw.Draw(im)
        colors = draw_utils.random_colors(n=len(bb_list))
        i = 0
        for BB in bb_list:
            ''' draw rectangle on image'''
            draw.rectangle(BB, fill = None, outline=colors[i], width = 2)
            i+=1
            #TODO ajouter l'indice de confiance
        if show_image:
                im.show()
        if saving_file:
            im.save(os.path.join(output_path, image[:-4]+"_prediction.png"))

def annotation_files_generation(model: str, image_path: str, output_path: str):
    """
    Generate YOLO annotation files for all images of a folder

    :param model: loaded YOLO model
    :param image_path: Path to images
    :param output_path: Path to saving annotations files
    """
    start = time.time()
    # Créer le dossier d'annotations s'il n'existe pas
    if not os.path.exists(output_path):
        os.mkdir(output_path) #TODO: si output_path doesn't exist

    # Itérer sur chaque image dans le dossier
    for image in os.listdir(image_path):
        print(image)
        predictions, resolution = extract_pred_bb(image_path=image_path, 
                        image = image,
                        model_name=model)
        if predictions:
            # Définir le chemin du fichier d'annotation
            base_name, _ = os.path.splitext(image)
            file_name = f'{base_name}.txt'
            chemin_fichier = os.path.join(output_path, file_name)
            # Écrire les annotations
            utils.write_yolo_annotation_file(predictions, chemin_fichier, resolution)
            print(f"predicted annotations completed for image {image}")
        else:
            pass
    end = time.time()
    # timer result
    length = end - start
    print(f"timer: {length}")


# ----------------------- ROI DETECTIONS ------------------------------------

def in_roi(box: list[float, float, float, float],roi: list[int, int, int, int]) -> bool:
    '''
    check if a bounding box is into ROI

    :params box: bounding box coordinates (x1, y1, x2, y2, conf, cls)
    :type box: list
    :params roi: ROI coordinates (rx1, ry1, rx2, ry2)
    :type roi: list
    '''
    if len(box)>5:
        x1, y1, x2, y2, conf, cls = box
    elif len(box)==4:
        x1, y1, x2, y2 = box
    else:
        x1, y1, x2, y2, cls = box
    rx1, ry1, rx2, ry2 = roi
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    return rx1 <= cx <= rx2 and ry1 <= cy <= ry2

def show_roi(im_path: str, roi: list, gt_roi: list, det_roi: list) -> None:
    '''
    show bndbox on a ROI on a image

    :params im_path: Path to image
    :type im_path: str
    :params roi: ROI coordinates (rx1, ry1, rx2, ry2)
    :type roi: list
    :params gt_roi: ground truth coordinates
    :type gt_roi: list
    :params det_roi: prediction coordinates 
    '''
    im = Image.open(im_path)
    # affichage de l'image
    draw = ImageDraw.Draw(im)
    draw.rectangle(roi, fill=None, outline=None, width=2)
    for box in gt_roi:
        draw.rectangle(box[:4], fill=None, outline="blue", width=2)
    for box in det_roi:
        print(box[:4])
        draw.rectangle(box[:4].tolist(), fill=None, outline="red", width=2)
    im.show()

def roi_det_info(img_path: str, model: str, roi: list[int, int, int, int], show: bool = True) -> dict:
    '''
    From a repository in an architecture with "images/" and "labels/",
    Predict detections into a ROI with a model and compare result with 
    ground truth.
    Output is a dictionary with name of image and Pr and Rc
    
    :param img_path: path to image
    :type img_path: str
    :param model: loaded detection model
    :type model: str
    :param roi: Region of interest coordinates (rx1, ry1, rx2, ry2)
    :type roi: list[int, int, int, int]
    :param img_size: resolution of image file (height, width)
    :type img_size: tuple(int, int)
    '''
    dict_result = {}

    for image in os.listdir(f'{img_path}/images/'):
        # open each image on img_path and predict 
        print("#####")
        print(image)
        
        img = Image.open(f'{img_path}/images/{image}')
        img_size = img.size  # (width, height)
        width, height = img_size
        # If you need (height, width) to match YOLO conventions:
        img_size = (height, width)

        # load predictions on one image
        results = model(f'{img_path}/images/{image}')
        boxes = []
        for result in results:
            boxes = result.boxes.data

        # load gt for one image
        bblist = utils.txt_extraction(f'{img_path}/labels/', f'{image[:-4]}.txt')
        gt_boxes = utils.convert_yolo_coco(bblist,img_size)

        detections_in_roi = [box for box in boxes if in_roi(box, roi)]
        ground_truths_in_roi = [box for box in gt_boxes if in_roi(box, roi)]

        # show roi and GT and predict bounding boxes
        if show:
            show_roi(f'{img_path}/images/{image}', roi, ground_truths_in_roi, detections_in_roi)

        # filter on ROI
        if len(detections_in_roi)>0:
            detections_in_roi = torch.stack(detections_in_roi)
        else:
            detections_in_roi = torch.empty((0, *boxes[0].shape))  # tensor vide avec même shape
        if len(ground_truths_in_roi)>0:
            ground_truths_in_roi = torch.tensor(ground_truths_in_roi)
        else:
            ground_truths_in_roi = torch.empty((0, *boxes[0].shape))  # tensor vide avec même shape

        #TODO : second function ? 
        # get only the coordinates values on gt_boxes
        gt_boxes  = ground_truths_in_roi[:, 0:4] if ground_truths_in_roi.shape[1] == 5 else ground_truths_in_roi[:, :4]
        
        # list of class object for each instance of gt_boxes if cls empty, fill it with 0
        gt_cls = ground_truths_in_roi[:, 4].int() if ground_truths_in_roi.shape[1] == 5 else torch.zeros(len(ground_truths_in_roi), dtype=torch.int)
        # confusion matrix call
        cm = ConfusionMatrix(nc=1)
        cm.process_batch(detections_in_roi, gt_boxes, gt_cls)  

        # precision and recall metrics
        tp = cm.matrix.diagonal()[:-1]      # vrais positifs [0,0]
        fp = cm.matrix[-1, :-1]             # faux positifs [0,1]
        fn = cm.matrix[:-1, -1]             # faux négatifs [1,0]
        precision = tp / (tp + fp + 1e-9)
        recall = tp / (tp + fn + 1e-9)
        # saving precision and recall for ROI
        dict_result[image] = [precision.item(),recall.item()]
        print("done")
    return(dict_result)
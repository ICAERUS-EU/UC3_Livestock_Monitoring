import json
import os
import pandas as pd
import cv2
from . import utils
# from .plot import plot_box_cv2

def get_labels_from_json(path) -> pd.DataFrame:
    """
    Load results from ultralytics in a data frame. Each row corresponding to a bounding
    box.
    Format expected in input xywh.

    Returns
    -------
        Dataframe with the corresponding bbox informations, in xywh format.
    """

    with open(path, "r") as f:
        labels = json.load(f)

    df = pd.DataFrame(labels)

    return df.groupby('image_id').aggregate( lambda x : list(x) )



def read_yolo_txt_file(path, scaling) -> pd.DataFrame:
    """
    Read annotation from yolov8 formatted annotation file.

    Parameters
    ----------
    path : str
        Input file to read annotation from.
    scaling : tuple 
        (height,weight)

    Returns
    -------
    Dataframe[N,6] 
        image_id, category_id, bbox. bbox of format cxcywh
        with N the number of annotated object.
    """
    cols = ["category_id", "cx", "cy", "w", "h"]
    labels = pd.read_csv(path, sep=" ", names=cols)
    labels['cx'] = labels['cx'] * scaling[1]
    labels['w'] = labels['w'] * scaling[1]
    labels['cy'] = labels['cy'] * scaling[0]
    labels['h'] = labels['h'] * scaling[0]
    
    labels['bbox'] = labels[['cx','cy','w','h']].apply(lambda x : list(x), axis=1)
    labels.drop(columns=['cx','cy','w','h'], inplace=True)
    #boxes = box_cxcywh_to_xyxy(boxes)

    labels.reset_index(inplace=True)
    return labels


def get_labels_from_yolo(path, scaling: int | list =None):
    """
    Read all yolo annotations on the specified directory 
    """
    files = [f for f in os.listdir(path) if f.endswith(".txt")]

    if isinstance(scaling, list):
        assert len(scaling) == len(files)

    labels = []
    for file in files:
        if not scaling :
            path_img = (
                path + os.sep + ".." + os.sep + "images" + os.sep + file[:-4] + ".jpg"
            )
            scale = cv2.imread(path_img).shape[:2]
        elif isinstance(scaling, list) :
            scale = scaling.pop(0)
        else:
            scale = scaling
        im_lab = read_yolo_txt_file(path + os.sep + file, scale)
        im_lab = (
            im_lab
            .groupby(lambda x : os.path.basename(file.replace(".txt", "")))
            .aggregate(list))
        labels.append(im_lab)

    return pd.concat(labels, ignore_index=True)

def write_tracking_results(result_iterator, save_path_txt, video_output_stream = None):
    """
    Write Ultralytics detection results in MOT format. If video stream is provided draw the boxes on it.

    Parameters
    ----------
    result_iterator
        Ultralytics result object.
    save_path_txt : str
        Name of the annotation path to save.
    video_output_stream 
        cv2 vidcap object.
    """
    results_to_save = list()
    for frame_nr, results in enumerate(result_iterator,start=1):
        frame = results.orig_img
        bboxes = results.boxes

        # skip frame if no results
        if results is None:
            continue

        for box in bboxes.data.cpu().numpy():
            idx = int(box[-3])
            x1, y1, x2, y2 = box[:4]
            w = x2-x1
            h = y2-y1

            if video_output_stream : 
                utils.plot.images.plot_box_cv2(frame,box[:4])
            # MOT format : <frame>, <id>, <bb_left>, <bb_top>, <width>, <height>,
            #              <conf>, <x>, <y>, <z>
            results_to_save.append([frame_nr, idx, x1,y1,w,h, box[-2],-1,-1,-1])

        # save tracking results
        with open(save_path_txt, "w") as f:
            for res in results_to_save:
                f.write(", ".join([str(r) for r in res]) + "\n")

        # write video frame
        if video_output_stream :
            video_output_stream.write(frame)

def load_frame_i(videocap, i):
    videocap.set(cv2.CAP_PROP_POS_FRAMES, i - 1)
    _, frame = videocap.read()
    return frame

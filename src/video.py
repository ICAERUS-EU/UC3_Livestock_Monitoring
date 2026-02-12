'''
Functions for video manipulation
'''
from moviepy import VideoFileClip, vfx
import os 
import cv2
from tqdm import tqdm

def video_modification(video_path: str, file_name: str,  end: int, begin : int = 0, number_frame: int = None, output_path: str = None, resolution: tuple = None, resize:float = None) -> None:
    '''
    Modification of video like change of duration, fps and/or resolution
    
    :param video_path: directory path through file_name
    :type video_path: str
    :param file_name: video name to modify
    :type file_name: str
    :param begin: begin of crop (sec) or tuple of (min,sec), (hour,min,sec) (optional)
    :type begin: int
    :param end: end of crop (sec) or tuple of (min,sec), (hour,min,sec)
    :type end: int
    :param output_path: output path to save video (optional)
    :type output_path: str
    :param resolution: tuple with new resolution attempt (optional)
    :type resolution: tuple
    :param number_frame: nb of fps needed (optional)
    :type number_frame: int
    '''
    # cropped video creation
    video = VideoFileClip(os.path.join(video_path,file_name)).subclipped(begin,end)
    print("fps : ", video.fps)
    base_name, _ = os.path.splitext(file_name)
    # resize video
    if resolution:
        video = video.resized(resolution)
    
    if resize:
        video = video.with_effects([vfx.Resize(resize)])

    name = f"crop_{base_name}_{number_frame}fps.MP4"
    if number_frame:
        if not output_path:
            video.write_videofile(os.path.join(video_path,name),fps = number_frame)
        else:
            video.write_videofile(os.path.join(output_path,name),fps = number_frame)
    if not number_frame:
        if not output_path:
            video.write_videofile(os.path.join(video_path,name))
        else:
            video.write_videofile(os.path.join(output_path,name))

def zoom_video(video_path: str, 
               file_name: str,  
               coor_x:int|float, 
               coor_y:int|float, 
               zoom_in: int,
               end: int, 
               begin : int = 0, 
               output_path: str = None) -> None:
    '''
    Crop on a specific part of a video depending on x and y coordinates (centers) and zoom_in factor
    
    :param video_path: path to video
    :type video_path: str
    :param file_name: file name
    :type file_name: str
    :param coor_x: center coordinates of x 
    :type coor_x: int
    :param coor_y: center coordinates of y
    :type coor_y: int
    :param zoom_in: factor of zoom
    :type zoom_in: int
    :param end: end of video (in sec)
    :type end: int
    :param begin: beginnig of video (in sec)
    :type begin: int
    :param output_path: output_path
    :type output_path: str
    '''
    base_name, _ = os.path.splitext(file_name)
    # reduce video duration
    clip = VideoFileClip(os.path.join(video_path,file_name)).subclipped(begin, end)

    w,h = clip.size

    w_zoom = int(w/zoom_in)
    h_zoom = int(h/zoom_in)
    coordinate_x = w/coor_x
    coordinate_y = h/coor_y
    # zoom in on video
    zoomed = clip.with_effects([
        vfx.Crop(x_center=coordinate_x, y_center = coordinate_y, width = w_zoom, height = h_zoom),
    ])

    name = f"zoom_{base_name}.MP4"

    zoomed.write_videofile(os.path.join(output_path,name))

def extraction_all_frames(video_path : str, file_name : str, resolution : tuple[int,int] | None = None) -> None:
    '''
    export all frames from a movie into jpg files

    :param video_path : path to movie
    :param file_name : name of movie 
    :param resolution: Optional (width, height) for the output image.
    :type resolution: tuple(int, int)
    '''
    base_name, _ = os.path.splitext(file_name)

    # output file
    output_folder = f'{os.path.join(video_path,base_name)}_frames'
    os.makedirs(output_folder, exist_ok=True)

    # read video
    video = os.path.join(video_path, file_name)
    cap = cv2.VideoCapture(video)

    frame_count = 0
    success = True

    while success:
        success, frame = cap.read()
        if success:
            # create file name with frame number 
            filename = os.path.join(output_folder, f'{base_name}_frame_{frame_count:06d}.jpg')
            if resolution is not None:
                frame = cv2.resize(frame, resolution)
            cv2.imwrite(filename, frame)
            print(f'Saved: {filename}')
            frame_count += 1

    cap.release()
    print("Success")

def extract_frame(
        video_path:str, 
        file_name:str, 
        second:int, 
        resolution: tuple[int, int] | None = None,
        output_path:str | None = None
        ) -> None:
    '''
    Extract a particular frame from a movie

    :param video_path: Directory containing the video file.
    :type video_path: str
    :param file_name: Video file name (e.g. 'video.mp4').
    :type file_name: str
    :param second: Second of the video from which to extract the frame (from 0).
    :type second: int
    :param resolution: Optional (width, height) for the output image.
    :type resolution: tuple(int, int)
    :param output_path: Optional directory to save the image. Defaults to video_path.
    :type output_path: str
    '''

    # path to video file
    video_file = os.path.join(video_path, file_name)
    # create videocapture object
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        raise ValueError("Can't open video file")
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps <= 0:
        cap.release()
        raise ValueError("Invalid FPS value (<=0) in video.")

    # select frame to extract
    frame_number = int(round(fps * second))

    # catch frame to extract
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # read frame to extract
    ret, frame = cap.read()
    if not ret or frame is None:
        cap.release()
        raise ValueError(f"Can't read the frame {frame_number}")

    if resolution is not None:
        frame = cv2.resize(frame, resolution)
    
    save_dir = output_path if output_path is not None else video_path

    base_name, _ = os.path.splitext(file_name)
    image_name = os.path.join(save_dir, f'{base_name}_frame_{frame_number:06d}.jpg')

    cv2.imwrite(image_name, frame)
    # Release resources
    cap.release()
    print(f"{frame_number} saved in: {save_dir}")

def interpolation_img(img_path, new_resolution: tuple[int,int], output_path: str, interpolation: str = 'nearest', show: bool = False):
    '''
    Crop image into using given new width and height and using an interpolation method to process.
    
    :param img_path: path to image
    :param new_resolution: new width and heights 
    :param output_path: images storage path
    '''
    
    # Define different scaling factors for width and height
    new_width = new_resolution[0]
    new_height = new_resolution[1]

    output_folder = f'{output_path}_{new_width}_{new_height}'
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the image
    for image in os.listdir(img_path):  
        im = cv2.imread(os.path.join(img_path,image))

        # Apply different interpolation methods
        #resized_area = cv2.resize(image, dsize = (new_width,new_height), interpolation=cv2.INTER_AREA)
        #resized_linear = cv2.resize(image, dsize = (new_width,new_height), interpolation=cv2.INTER_LINEAR)
        #resized_cubic = cv2.resize(image, dsize = (new_width,new_height), interpolation=cv2.INTER_CUBIC)
        resized_nearest = cv2.resize(im, dsize = (new_width,new_height), interpolation=cv2.INTER_NEAREST)

        base_name, _ = os.path.splitext(image)
        image_name = os.path.join(output_folder, f'{base_name}_{new_width}-{new_height}.jpg')

        cv2.imwrite(image_name, resized_nearest)
        # Release resources
        print(f"{image_name} saved in: {output_folder}")
        
        # Display the resized images
        if show:
            cv2.imshow("Resized with INTER_NEAREST", resized_nearest)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def tile_image(image_path: str, 
               image: str, 
               output_path: str,
               row,
               col,
               new_resolution: tuple[int, int] = None, 
               show: bool = False, 
               save: bool = False) -> None:
    '''
    Tile image into its center and apply a reshape if notated
    
    :param image_path: Path to image directory
    :type image_path: str
    :param image: image name
    :type image: str
    :param output_path: saving directory
    :type output_path:str
    :param new_resolution: New resolution
    :type new_resolution: tuple[int, int]
    :param show: show image if true
    :type show: bool
    :param save: save image if true
    :type save: bool
    '''
    os.makedirs(output_path, exist_ok=True)
    base_name, _ = os.path.splitext(image)
    img = cv2.imread(os.path.join(image_path,image))
    numrows, numcols = 3, 3
    height = int(img.shape[0] / numrows)
    width = int(img.shape[1] / numcols)
    y0 = row * height
    y1 = y0 + height
    x0 = col * width
    x1 = x0 + width
    tile_img = img[y0:y1, x0:x1]
    resized_img = cv2.resize(src = tile_img, dsize=new_resolution, interpolation=cv2.INTER_NEAREST)
    if show :
        cv2.imshow("tile_img", resized_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if save: 
        save_name = f'{base_name}_tile_{new_resolution[0]}_{new_resolution[1]}.jpg'
        cv2.imwrite(os.path.join(output_path,save_name), resized_img)
    '''
    for row in range(numrows):
        for col in range(numcols):
            y0 = row * height
            y1 = y0 + height
            x0 = col * width
            x1 = x0 + width
            cv2.imwrite('tile_%d%d.jpg' % (row, col), img[y0:y1, x0:x1])
    '''
    #cv2.imwrite('tile_%d%d.jpg' % (row, col), img[y0:y1, x0:x1])
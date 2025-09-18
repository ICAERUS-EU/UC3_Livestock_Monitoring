#  🐏 Sheep Counting Using Object Detection and ByteTrack

##  🌍 Overview

These Jupyter Notebooks provides a practical solution for counting sheep in video footage using advanced object detection and tracking technologies. Inspired by the techniques and resources from the Supervision GitHub repository, the notebook outlines a step-by-step approach to load a pre-trained model for object detection and then track and count sheep as they pass a virtual line or a polygon zone using ByteTrack. The `count_sheep_line` notebook is an application of the tutorial [Count Objects Crossing the Line](https://supervision.roboflow.com/develop/notebooks/count-objects-crossing-the-line/) from Supervision.
The `count_sheep_polygon` notebook is an application of the tutorial [How To Analyze Occupancy](https://supervision.roboflow.com/develop/notebooks/occupancy_analytics/#install-relevant-packages) from Supervision.

The primary objectives of this notebook are:

1. **Loading and Deploying an Object Detection Model**: We will begin by loading one of the pre-trained sheep detecting models.

2. **Evaluating Model Performance on Video**: After loading the detection model, we will apply it to a sample video of a flock of sheep. This step involves processing each frame to identify and classify sheep.

3. **Tracking Sheep with ByteTrack**: We use ByteTrack to follow each sheep across frames. ByteTrack is designed to maintain tracking of objects even in crowded or occluded scenarios, ensuring consistent identification and tracking of each sheep.

4. **Counting Sheep Crossing a Virtual Line**: A virtual line is added in the video frame and count how many sheep cross this line. 

5. **Record video with sheep counting**: All the previous steps are combined to produce a video in which sheep are counted.

## 💻 Requirement

Using the requirements.txt file: use pip or conda using one of these commands:

`pip install -r requirements.txt`

`conda create --name <env> --file requirements.txt`



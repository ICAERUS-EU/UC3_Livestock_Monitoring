<div align="center">
  <p>
    <a href="https://icaerus.eu" target="_blank">
      <img width="50%" src="https://raw.githubusercontent.com/ICAERUS-EU/.github/refs/heads/main/profile/ICAERUS_transparent.png"></a>
    <h3 align="center">UC3 Livestock Monitoring 🐄🐏 </h3>
    
   <p align="center">
    <br/>
    <a href="https://github.com/icaerus-eu/UC3_Livestock_Monitoring/wiki"><strong>Explore the wiki »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/icaerus-eu/UC3_Livestock_Monitoring/issues">Report Bug</a>
    -
    <a href="https://github.com/icaerus-eu/UC3_Livestock_Monitoring/issues">Request Feature</a>
  </p>
</p>
</div>

![Downloads](https://img.shields.io/github/downloads/icaerus-eu/UC3_Livestock_Monitoring/total) ![Contributors](https://img.shields.io/github/contributors/icaerus-eu/UC3_Livestock_Monitoring?color=dark-green) ![Forks](https://img.shields.io/github/forks/icaerus-eu/UC3_Livestock_Monitoring?style=social) ![Stargazers](https://img.shields.io/github/stars/icaerus-eu/UC3_Livestock_Monitoring?style=social) ![Issues](https://img.shields.io/github/issues/icaerus-eu/UC3_Livestock_Monitoring) ![License](https://img.shields.io/github/license/icaerus-eu/UC3_Livestock_Monitoring) 

## Table Of Contents
- [Summary](#summary)
- [Structure](#structure)
- [Models](#models)
- [Application](#application)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Summary
We propose an use of UAV images and videos to automatically recognize and count animals in extensive areas. 

Four computer vision models are currently in this repository:
- Two models for cow recognition from UAV images in nadir position.
- Two models for sheep recognition from UAV videos.

An application script using the sheep detection model is also available for counting sheep in the video.

More details on models section.

## Structure

The repository folders are structured as follow:

- **data**: some example videos and images to use application scripts. You can find on Zenodo others [sheep video](https://zenodo.org/records/10400302) and [cow images](https://zenodo.org/records/8234156) that you could download and add to data repository to test models and application scripts.
- **models:** models developed for aerial animals detection.
- **appplication:** application scripts using sheep models to count animals.
- **platform.json:** organized information about the models.

## Models

The [models](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/models) developed are the following:

#### _[Cow detection model in aerial view with YOLOv8 - Large images](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/models/cow_detection/cow_detection_v1)_
The model has been trained with YOLOv8 and is capable of detecting cow at a height of 100 meters from large images (resolution > 3000x4000 px).

#### _[Cow detection model in aerial view with YOLOv8 - Mosaic images](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/models/cow_detection/cow_detection_v2)_
The model has been trained with YOLOv8 and is able to detect cows from large images divided into several small images (resolution = 640x640 px).

#### _[Sheep detection model in aerial view with YOLOv8 - version 1](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/models/sheep_detection/yolo8m_sheep_v1)_
The model has been trained with YOLOv8 and is able to detect sheep at a height of 5 to 10 meters.

#### _[Sheep detection model in aerial view with YOLOv8 - version 2](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/models/sheep_detection/yolo8m_sheep_v2)_
The model has been trained with YOLOv8 and is able to detect sheep at a height of 5 to 10 meters. The dataset used to train the model is different from the previous one.

#### _[Sheep detection model in aerial view using YOLOv11n](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/models/sheep_detection/yolo11n_sheep)_
The model has been trained with the lightest version of YOLOv11 and is capable of detecting sheep at a height of 5 to 10 meters. This model detects animals faster than other versions of yolo11 and will be more interesting to deploy.

#### _[Sheep detection model in aerial view using YOLOv11s](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/models/sheep_detection/yolo11s_sheep)_
The model has been trained with a light version of YOLOv11 and is capable of detecting sheep at a height of 5 to 10 meters. This model combines fast execution compared to yolov11m and good detection of animals compared to yolov11n.

## Application

#### _[Notebooks](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/application/notebooks)_
The script uses one of the sheep detection models, then tracks and counts sheep crossing a field on the video. 

#### _[Deployment tools for sheep counting](https://github.com/ICAERUS-EU/UC3_Livestock_Monitoring/tree/main/application/deployment)_
This folder contains two separate deployment tools for the sheep counting application:
- **End-User Deployment**: Designed for end users, this tool provides a simple and ready-to-use setup for running the application.
- **Researcher Deployment**: Aimed at researchers, this tool makes it easy to set up local videos of sheep counting for testing, development, and customization.

These two deployment modes ensure both ease of use for non-technical users and flexibility for researchers.

## Authors
- Louise Helary - Institut de l'Elevage (IDELE) - [Louise Helary](https://github.com/louisehelary)
- Madeline Le Pors - Institut de l'Elevage (IDELE) - [Madeline Le Pors](https://github.com/madelinelepors)

## Acknowledgments
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>

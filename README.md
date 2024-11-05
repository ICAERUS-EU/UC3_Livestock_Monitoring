<div align="center">
  <p>
    <a href="https://icaerus.eu" target="_blank">
      <img width="50%" src="https://icaerus.eu/wp-content/uploads/2022/09/ICAERUS-logo-white.svg"></a>
    <h3 align="center">UC3 Livestock Monitoring </h3>
    
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
- [Models](#models)
  - [Cow detection](#cowdetection)
  - [Sheep detection](#sheepdetection)
- [Application](#application)
  - [Sheep counting](#sheep_counting)
- [Acknowledgments](#acknowledgments)

## Summary
We propose an use of UAV images and videos to automatically recognize and count animals in extensive areas. 

Two computer vision models are currently in development:
- A model for cow recognition and counting from UAV images in nadir position.
- A model for sheep recognition and counting from UAV videos.

## Models

### Cow detection
Cow detection models have been developed using YOLOv8-n pre-trained model from ultralytics.

Two models are available in the model repository, more details in this one.

### Sheep detection
Sheep detection models have been developed using YOLOv8-m pre-trained model from ultralytics.

Two models are available in the model repository, the first being the best.

## Application

### Sheep counting
Sheep detection model can be used to track and count sheep crossing a field on video. 

## Acknowledgments
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>

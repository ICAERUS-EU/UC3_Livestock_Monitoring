# 🐑 Deployment Tools for Sheep Counting

This folder contains two deployment tools for a sheep counting application that processes video input.

The application allows users to:
- Upload a video
- Trim its duration
- Reduce its resolution
- Draw a reference line used for counting sheep

## 🧑‍💼 End-User Deployment (count_sheep_developer)

Provides a streamlined interface for non-technical users to process videos with default settings. Ideal for production use, with minimal configuration required.

## 🛠️ Development Deployment (count_sheep_user)

Offers additional flexibility for developers, including:

- Customizing the frame rate (FPS)
- Selecting different sheep detection models

These two deployment modes ensure ease of use for end users and full control for developers.

## 📁 Data Preparation

Step-by-step instructions for preparing your videos and using the application are available in the `UI_protocol_demonstrator.pdf` file included in this folder.
It covers everything from installing Python to importing a video and to drawing the counting line and launching the processing.

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import (QMessageBox)

class LineDrawer:
    def __init__(self, label, crop_button, line_button, input_video_path, offset_x, offset_y, temp_crop_rect, scale_x, scale_y, parent):
        self.first_frame_label = label
        self.crop_video_button = crop_button
        self.draw_line_button = line_button
        self.input_video_path = input_video_path
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.temp_crop_rect = temp_crop_rect
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.parent = parent



    def enable_line_drawing(self):
        # Only enable drawing if the button is enabled
        if not self.draw_line_button.isEnabled():
            return
        
        # Activate line drawing mode and clear any previously stored line points
        self.drawing_line = True
        self.line_points = []
        
        # Assign mouse events to handle drawing points       
        self.first_frame_label.mousePressEvent = self.capture_line_points
        
        self.draw_line_button.setStyleSheet("background-color: lightgray; color: gray;")
        self.crop_video_button.setStyleSheet("font-size: 16px;")
    

    def capture_line_points(self, event):
        # Exit if we’re not in drawing mode
        if not self.drawing_line:
            return


        # Get the X and Y position of the mouse click relative to the image
        x = event.pos().x() - self.offset_x
        y = event.pos().y() - self.offset_y

        # Make sure that the click is within the image boundaries
        if x < 0 or y < 0 or x >= self.first_frame_label.pixmap().width() or y >= self.first_frame_label.pixmap().height():
            return  

        # Make sure the click occurs within the cropping rectangle
        if self.temp_crop_rect and not self.temp_crop_rect.contains(x, y):
            QMessageBox.warning(self.parent, "Point en dehors du crop", "Veuillez cliquer à l'intérieur de la zone de crop.")
            return

        # Store the clicked point
        self.line_points.append((x,y))
        
        # Update the image with the current points
        self.draw_line_on_image()

        # Once two points are defined, disable drawing mode
        if len(self.line_points) == 2:
            self.drawing_line = False
            self.draw_line_button.setEnabled(False)

            # Convert coordinates to match the cropped and resized video
            # Step 1: Convert the clicked point from QLabel coordinates to original video coordinates
            x_video = x * self.scale_x
            y_video = y * self.scale_y

            # Step 2: Convert to coordinates relative to the crop area
            crop_x = self.temp_crop_rect.x() * self.scale_x
            crop_y = self.temp_crop_rect.y() * self.scale_y
            x_in_crop = x_video - crop_x
            y_in_crop = y_video - crop_y

            # Step 3: Scale to the 640x640 format
            crop_w = self.temp_crop_rect.width() * self.scale_x
            crop_h = self.temp_crop_rect.height() * self.scale_y
            scale_to_640_x = 640 / crop_w
            scale_to_640_y = 640 / crop_h

            self.video_line_points = []

            for point in self.line_points:
                # 1. Convert QLabel coords to full video coords
                x_video = point[0] * self.scale_x
                y_video = point[1] * self.scale_y

                # 2. Convert to crop-relative
                x_in_crop = x_video - crop_x
                y_in_crop = y_video - crop_y

                # 3. Scale to 640x640
                final_x = x_in_crop * scale_to_640_x
                final_y = y_in_crop * scale_to_640_y

                # Store the clicked point
                self.video_line_points.append((int(final_x), int(final_y)))
                self.parent.video_line_points = self.video_line_points
                
            
        


    def draw_line_on_image(self):
        pixmap = self.first_frame_label.pixmap()
        if pixmap is None:
            return

        # Copy the pixmap to draw on it
        pixmap_copy = pixmap.copy()
        painter = QPainter(pixmap_copy)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.red)

        radius = 3

        # Draw all the clicked points
        for point in self.line_points:
            painter.drawEllipse(point[0] - radius, point[1] - radius, radius * 2, radius * 2)

        # If 2 points: draw the line
        if len(self.line_points) == 2:
            p1, p2 = self.line_points
            painter.drawLine(p1[0], p1[1], p2[0], p2[1])
            self.draw_line_button.setStyleSheet("font-size: 16px;")

        painter.end()
        self.first_frame_label.setPixmap(pixmap_copy)

        
        
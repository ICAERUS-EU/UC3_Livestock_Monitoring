import os
import cv2
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import (QMessageBox, QProgressDialog, QApplication)

class VideoCropper(QObject):
    # Signal emitted when the cropped video is successfully saved
    crop_done = pyqtSignal(str)  
    
    def __init__(self, label, crop_button, line_button, input_video_path, selected_fps, offset_x, offset_y, scale_x, scale_y, crop_start_time, crop_end_time, parent):
        # Initialize the QObject with the parent widget
        self.parent = parent  
        super().__init__(parent) 

        # UI elements and configuration
        self.first_frame_label = label
        self.crop_video_button = crop_button
        self.draw_line_button = line_button
        self.input_video_path = input_video_path
        self.selected_fps = selected_fps
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.crop_start_time = crop_start_time
        self.crop_end_time = crop_end_time
        self.pixmap_before_crop = None
        self.temp_crop_rect = None
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.crop_video_path = "videos/crop_videos"

        


    def enable_crop_video(self):
        # Only enable crop if button is enabled
        if not self.crop_video_button.isEnabled():
            return
        
        # Reset crop-related state variables
        self.drawing_crop = False
        self.crop_start_point = None
        self.crop_end_point = None

        # Assign mouse events to handle cropping
        self.first_frame_label.mousePressEvent = self.start_crop
        self.first_frame_label.mouseMoveEvent = self.update_crop
        self.first_frame_label.mouseReleaseEvent = self.end_crop

        self.crop_video_button.setStyleSheet("background-color: lightgray; color: gray;")
        self.draw_line_button.setStyleSheet("font-size: 16px;")


    def start_crop(self, event):
        # Exit if crop button is not enabled
        if not self.crop_video_button.isEnabled():
            return
    
        # Begin drawing: store the starting point and prepare for drawing
        self.drawing_crop = True
        self.crop_start_point = QPoint(event.pos().x() - self.offset_x, event.pos().y() - self.offset_y)
        self.crop_end_point = self.crop_start_point

        # Backup the original pixmap to restore between updates
        self.pixmap_before_crop = self.first_frame_label.pixmap().copy()

        # Draw initial rectangle
        self.draw_crop_rectangle()
    

    def update_crop(self, event):
        # Only update the rectangle if user is actively drawing
        if not self.drawing_crop:
            return

        end_point = QPoint(event.pos().x() - self.offset_x, event.pos().y() - self.offset_y)

        # Calculate the difference between current point and start point
        dx = end_point.x() - self.crop_start_point.x()
        dy = end_point.y() - self.crop_start_point.y()

        # Take the direction (up/left or down/right)
        side = min(abs(dx), abs(dy))
        dx_sign = 1 if dx >= 0 else -1
        dy_sign = 1 if dy >= 0 else -1

        # Calculate new end_point to enforce a square shape
        self.crop_end_point = QPoint(
            self.crop_start_point.x() + dx_sign * side,
            self.crop_start_point.y() + dy_sign * side
        )

        # Redraw the temporary crop rectangle
        self.draw_crop_rectangle()


    def end_crop(self, event):
        # Finalize the crop area when the mouse button is released
        if not self.drawing_crop:
            return
        
        end_point = QPoint(event.pos().x() - self.offset_x, event.pos().y() - self.offset_y)
        dx = end_point.x() - self.crop_start_point.x()
        dy = end_point.y() - self.crop_start_point.y()

        side = min(abs(dx), abs(dy))
        dx_sign = 1 if dx >= 0 else -1
        dy_sign = 1 if dy >= 0 else -1

        # Finalize the crop end point as a square
        self.crop_end_point = QPoint(
            self.crop_start_point.x() + dx_sign * side,
            self.crop_start_point.y() + dy_sign * side
        )

        self.drawing_crop = False
        self.draw_crop_rectangle(final=True)

        # Restore crop button style to normal
        self.crop_video_button.setStyleSheet("font-size: 16px;")
        self.crop_video_button.setEnabled(False)
        self.draw_line_button.setEnabled(True)


    def draw_crop_rectangle(self, final=False):
        # Exit if any necessary variable is missing
        if self.pixmap_before_crop is None or self.crop_start_point is None or self.crop_end_point is None:
            return

        # Make a copy of the original image
        pixmap_copy = self.pixmap_before_crop.copy()

        # Setup the painter with a dashed rectangle, green if final, yellow if in progress
        painter = QPainter(pixmap_copy)
        pen = QPen(Qt.green if final else Qt.yellow, 2, Qt.DashLine)
        painter.setPen(pen)

        # Create and normalize the rectangle (ensures positive width/height)
        rect = QRect(self.crop_start_point, self.crop_end_point)
        painter.drawRect(rect.normalized())
        if not final:
            # Calculate dimensions in the video space
            crop_w = int(rect.width() * self.scale_x)
            crop_h = int(rect.height() * self.scale_y)

            # Text to display
            text = f"{crop_w}px x {crop_h}px"

            # Position of the text
            text_x = rect.left() 
            text_y = rect.bottom() 
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 10, QFont.Bold))

            painter.drawText(text_x, text_y, text)
        
        else :
            # Calculate dimensions in the video space
            crop_w = int(rect.width() * self.scale_x)
            crop_h = int(rect.height() * self.scale_y)

            # Text to display
            text = f"{crop_w}px x {crop_h}px"

            # Position of the text
            text_x = rect.left() 
            text_y = rect.bottom() 
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 10, QFont.Bold))

            painter.drawText(text_x, text_y, text)

        painter.end()

        # Display the updated image with the drawn rectangle
        self.first_frame_label.setPixmap(pixmap_copy)

        if final:
            # If this is the final crop, store the rectangle for future processing
            self.pixmap_before_crop = pixmap_copy
            self.temp_crop_rect = rect.normalized()

            self.parent.temp_crop_rect = self.temp_crop_rect
        

    

    def crop_and_export_video(self):
        # Ensure start and end times are set
        if not hasattr(self, 'crop_start_time') or not hasattr(self, 'crop_end_time'):
            QMessageBox.warning(self.parent, "Attention", "Veuillez d'abord définir un temps de début et de fin avant d'exporter.")
            return
        
        # Ensure a crop rectangle has been defined
        if not hasattr(self, 'temp_crop_rect') or self.temp_crop_rect is None:
            QMessageBox.warning(self.parent, "Attention", "Veuillez d'abord dessiner une zone de crop sur la vidéo.")
            return
    
        # Show a modal progress dialog
        progress = QProgressDialog("Modifications de la vidéo en cours…", None, 0, 0, self.parent)
        progress.setWindowTitle("Loading...")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumWidth(400) # Set dialog width
        progress.setMaximumHeight(200) # Set dialog height
        progress.setSizeGripEnabled(True) # Allow manual resizing by the user
        progress.setCancelButton(None)  # no cancel button
        progress.setRange(0, 0) # Set bouncing effect of the progress bar
        progress.show()
        QApplication.processEvents()

    

        # Get QLabel display size
        label_width = self.first_frame_label.width()
        label_height = self.first_frame_label.height()

        # Open the input video and read the first frame to get real video dimensions
        cap = cv2.VideoCapture(self.input_video_path)
        ret, frame = cap.read()
        if not ret:
            QMessageBox.critical(self, "Error", "Can't read first frame.")
            cap.release()
            return
        video_height, video_width = frame.shape[:2]

        
        # Convert the crop rectangle from QLabel coordinates to actual video coordinates
        crop_x = int(self.temp_crop_rect.x() * self.scale_x)
        crop_y = int(self.temp_crop_rect.y() * self.scale_y)
        crop_w = int(self.temp_crop_rect.width() * self.scale_x)
        crop_h = int(self.temp_crop_rect.height() * self.scale_y)

        
        # Define target resolution for output video
        target_width = 640
        target_height = 640

        # Ensure crop region stays within video bounds
        if crop_x + crop_w > video_width or crop_y + crop_h > video_height:
            QMessageBox.critical(self, "Error", "Crop video out of dimensions.")
            cap.release()
            return

        # Prepare export settings
        output_fps = self.selected_fps
        #video_path = os.path.dirname(self.crop_video_path)
        crop_video_path = os.path.normpath(os.path.join(self.crop_video_path, f"sheep_crossing_{output_fps}fps_{target_width}px.avi"))

        # Compute how often to grab frames
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(round(original_fps / output_fps)) if original_fps > output_fps else 1

        # Convert start/end times to frame indices
        start_frame = int(self.crop_start_time * original_fps)
        end_frame = int(self.crop_end_time * original_fps)

        # Seek to the start frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') #"mp4v" 'XVID'
        out = cv2.VideoWriter(crop_video_path, fourcc, output_fps, (target_width, target_height))

        # Process frames within the selected time range
        frame_count = start_frame
        while frame_count < end_frame:
            ret, frame = cap.read()
            if not ret:
                break # End of video

            if frame_count % frame_interval == 0:
                # Crop the frame based on user's selection
                cropped_frame = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]

                # Resize the cropped frame to the target resolution (640x640)
                resized_frame = cv2.resize(cropped_frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
                
                if resized_frame.shape[0] != 640 or resized_frame.shape[1] != 640:
                    print("Crop out of bounds, skipping frame.")
                    continue

                # Write the processed frame to output video
                out.write(resized_frame)

            frame_count += 1

            # Force the UI to update so progress bar animation moves
            QApplication.processEvents()

        cap.release()
        out.release()
        progress.close()

        QMessageBox.information(self.parent, "Success", f"Video has been released!\n Path to video :\n{crop_video_path}")
        self.parent.crop_video_path = crop_video_path
        self.crop_done.emit(crop_video_path)

    












# ============================================================================================================
#                   🐑 Bienvenue dans le projet de comptage de mouton par IA & drone🐑
#          Ce fichier permet d'ouvrir une interface afin de compter les moutons via des vidéos drones
#                          sans que vous ayez à plonger dans le code compliqué.
# ============================================================================================================








 
 
 
 
 
 
 
 
 
 
 
import sys
import cv2
from ffpyplayer.player import MediaPlayer
from sheep_detector import SheepDetector
from video_cropper import VideoCropper
from line_drawer import LineDrawer
from PyQt5.QtWidgets import ( QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QSpacerItem, QSizePolicy, QRadioButton, QButtonGroup, QMessageBox, QStackedWidget, 
    QProgressDialog, QFrame, QLineEdit)
from PyQt5.QtCore import Qt, QThread, QTimer, QRegularExpression
from PyQt5.QtGui import QImage, QPixmap, QRegularExpressionValidator
from PyQt5.QtMultimediaWidgets import QVideoWidget


class InterfaceApp(QWidget):
    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowTitle('ICAERUS')
        self.setGeometry(100, 100, 600, 400)


        # Default values
        self.selected_fps = 15   
        self.model_path = "models/yolo11n.pt"
        self.model_suffix = "11n"
        self.input_video_path = None
        self.drawing_crop = False
        self.crop_start_point = None
        self.crop_end_point = None
        self.temp_crop_rect = None
        self.video_line_points = []
        self.crop_video_path = None


        # Hello label
        self.hello_label = QLabel('Bonjour ! Prêt à compter les moutons ?')
        self.hello_label.setStyleSheet("font-size: 25px; color: #333;")
        self.hello_label.setAlignment(Qt.AlignCenter)
        self.hello_label.setWordWrap(True)


        # Video selection
        self.video_selection_label = QLabel('Choisissez une vidéo :')
        self.video_selection_label.setStyleSheet("font-size: 16px; color: #333;")
        self.video_selection_label.setAlignment(Qt.AlignCenter)
        self.video_selection_label.setWordWrap(False)


        # Label to display the selected video path
        self.input_video_path_label = QLabel('')
        self.input_video_path_label.setStyleSheet("font-size: 16px; color: #555;")
        self.input_video_path_label.setAlignment(Qt.AlignCenter)
        self.input_video_path_label.setWordWrap(True)


        # Button to choose a video file
        self.choose_video_button = QPushButton('Choisir une video')
        self.choose_video_button.setStyleSheet("font-size: 16px;")
        self.choose_video_button.clicked.connect(self.choose_video)



        # Start and Cancel visualisation buttons
        self.start_visu_button = QPushButton('Commencer')
        self.cancel_visu_button = QPushButton('Annuler')
        self.start_visu_button.setStyleSheet("font-size: 16px;")
        self.cancel_visu_button.setStyleSheet("font-size: 16px;")

        self.start_visu_button.clicked.connect(self.start_processing)
        self.cancel_visu_button.clicked.connect(self.clear_video)


        # Image and video preview
        self.first_frame_label = QLabel()
        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(640, 640)

        self.display_stack = QStackedWidget()
        self.display_stack.addWidget(self.first_frame_label) 
        self.display_stack.addWidget(self.video_widget)
        

        # Start/End time layout
        crop_layout = QHBoxLayout()
        crop_layout.setContentsMargins(0, 0, 0, 0)
        crop_layout.setSpacing(20)  

        # Start time input
        debut_container = QHBoxLayout()
        debut_container.setSpacing(2)  # Coller label et champ
        debut_label = QLabel("Début:")
        self.start_time_edit = QLineEdit()
        self.start_time_edit.setPlaceholderText("mm:ss")
        self.start_time_edit.setMaximumWidth(50)
        self.start_time_edit.setStyleSheet("""QLineEdit {border: none; font-size: 14px; padding: 0; 
        }""")
        debut_container.addWidget(debut_label)
        debut_container.addWidget(self.start_time_edit)

        # End time input
        fin_container = QHBoxLayout()
        fin_container.setSpacing(2)  # Coller label et champ
        fin_label = QLabel("Fin:")
        self.end_time_edit = QLineEdit()
        self.end_time_edit.setPlaceholderText("mm:ss")
        self.end_time_edit.setMaximumWidth(50)
        self.end_time_edit.setStyleSheet("""QLineEdit {border: none; font-size: 14px; padding: 0; 
        }""")
        fin_container.addWidget(fin_label)
        fin_container.addWidget(self.end_time_edit)

        # Apply time input validation (restricts user input to proper format)
        self.setup_time_fields()

        # Add start and end time inputs side by side
        crop_layout.addLayout(debut_container)
        crop_layout.addLayout(fin_container)
        crop_layout.addSpacing(100)

        # Create a widget container for the crop layout
        self.crop_widget = QWidget()
        self.crop_widget.setLayout(crop_layout)


        # Crop vido and draw line
        self.drawing_line = False
        self.line_points = []

        self.reduce_video_button = QPushButton("         Réduire ma vidéo        ")
        self.crop_video_button = QPushButton("          Rogner ma vidéo        ")
        self.draw_line_button = QPushButton(" Placer ma ligne de comptage ")
        self.reset_video_button = QPushButton("     Réinitialiser ma vidéo       ")
        
        for btn in [self.reduce_video_button, self.crop_video_button, self.draw_line_button, self.reset_video_button]:
            btn.setStyleSheet("font-size: 16px;")
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
        self.reduce_video_button.clicked.connect(self.reduce_video)
        self.crop_video_button.clicked.connect(self.crop_video)
        self.draw_line_button.clicked.connect(self.draw_line)
        self.reset_video_button.clicked.connect(self.reset_video)


        # Start and Cancel counting buttons
        self.start_counting_button = QPushButton('Commencer le comptage')
        self.cancel_counting_button = QPushButton('Annuler')
        self.start_counting_button.setStyleSheet("font-size: 16px;")
        self.cancel_counting_button.setStyleSheet("font-size: 16px;")

        self.cancel_counting_button.clicked.connect(self.cancel_counting)
        self.start_counting_button.setEnabled(False)


        # Print buttons when the frame is show
        self.crop_widget.hide()
        self.reduce_video_button.hide()
        self.crop_video_button.hide()
        self.draw_line_button.hide()
        self.reset_video_button.hide()
        self.start_counting_button.hide()
        self.cancel_counting_button.hide()
        



        ### LAYOUT ###

        # Layout for choose video button
        choose_video_layout = QHBoxLayout()
        choose_video_layout.addStretch()
        choose_video_layout.addWidget(self.video_selection_label)
        choose_video_layout.addSpacing(20)
        choose_video_layout.addWidget(self.choose_video_button)
        choose_video_layout.addStretch()


        # Layout for Start and Cancel visualisation buttons
        start_cancel_visu_layout = QHBoxLayout()
        start_cancel_visu_layout.addStretch()
        start_cancel_visu_layout.addWidget(self.start_visu_button)
        start_cancel_visu_layout.addSpacing(20)
        start_cancel_visu_layout.addWidget(self.cancel_visu_button)
        start_cancel_visu_layout.addStretch()

        # Layout for place and reset the counting line
        crop_line_button_layout = QVBoxLayout()
        crop_line_button_layout.addStretch()
        crop_line_button_layout.addWidget(self.crop_widget)
        crop_line_button_layout.addWidget(self.reduce_video_button)
        crop_line_button_layout.addWidget(self.crop_video_button)
        crop_line_button_layout.addWidget(self.draw_line_button)
        crop_line_button_layout.addSpacing(40)
        crop_line_button_layout.addWidget(self.reset_video_button)
        crop_line_button_layout.addStretch()

        # Layout to show the first frame + buttons to create the counting line
        image_and_tools_layout = QHBoxLayout()
        image_and_tools_layout.addStretch()
        image_and_tools_layout.addLayout(crop_line_button_layout)
        image_and_tools_layout.addSpacing(20)
        image_and_tools_layout.addWidget(self.display_stack)
        image_and_tools_layout.addSpacing(200)
        image_and_tools_layout.addStretch()

        # Layout for Start and Cancel counting buttons
        start_cancel_counting_layout = QHBoxLayout()
        start_cancel_counting_layout.addStretch()
        start_cancel_counting_layout.addWidget(self.start_counting_button)
        start_cancel_counting_layout.addSpacing(20)
        start_cancel_counting_layout.addWidget(self.cancel_counting_button)
        start_cancel_counting_layout.addStretch()

        # Top layout to keep everything at the top
        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        main_layout.addWidget(self.hello_label)
        main_layout.addSpacing(20)
        main_layout.addLayout(choose_video_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.input_video_path_label)
        main_layout.addSpacing(20)
        main_layout.addLayout(start_cancel_visu_layout)
        main_layout.addLayout(image_and_tools_layout)
        main_layout.addLayout(start_cancel_counting_layout)
        main_layout.addSpacerItem(QSpacerItem(0, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Push everything up
        
        self.setLayout(main_layout)

    


    def choose_video(self):
        # Open a file dialog to select a video
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une vidéo",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv)"
        )
        # If a file is selected, display its path
        if file_path:
            self.input_video_path = file_path
            self.input_video_path_label.setText(f"Vidéo selectionnée : {file_path}")
        else:
            self.input_video_path = None
            self.input_video_path_label.setText("Aucune vidéo sélectionnée")


    def clear_video(self):
        # Clear the video selection
        self.input_video_path_label.setText("")
        self.input_video_path = None
        # Hide all controls buttons and first frame display
        self.cancel_counting()


    def start_processing(self):
        # Display the input video to start the processing
        self.display_input_video()

        # Enable the reduce video button
        self.reduce_video_button.setEnabled(True)
        
        

    def display_first_frame(self, video_path):
        # Load the first frame from the given video file
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            self.first_frame_label.setText("Erreur de téléchargement de la première frame.")
            return

        # Convert BGR (OpenCV) to RGB (Qt)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w

        q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        # Store the original pixmap
        self.original_pixmap = pixmap

        # Save the original video dimensions
        self.video_height, self.video_width = frame.shape[:2]

        # Get the actual size of the QLabel on screen
        label_width = self.first_frame_label.width()
        label_height = self.first_frame_label.height()


        # Scale the pixmap proportionally to fit into the QLabel
        scaled_pixmap = pixmap.scaled(
            label_width,
            label_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        # Store the displayed pixmap and its dimensions
        self.displayed_pixmap = scaled_pixmap
        self.displayed_pixmap_width = scaled_pixmap.width()
        self.displayed_pixmap_height = scaled_pixmap.height()

        # Compute scaling factors between QLabel and original video size
        self.scale_x = self.video_width / self.displayed_pixmap_width
        self.scale_y = self.video_height / self.displayed_pixmap_height

        # Compute the offset relative to the QLabel (margins around the pixmap)
        self.offset_x = (label_width - self.displayed_pixmap_width) // 2
        self.offset_y = (label_height - self.displayed_pixmap_height) // 2
        
        # Display the scaled first frame on the QLabel
        self.first_frame_label.setPixmap(scaled_pixmap)
        self.display_stack.setCurrentWidget(self.first_frame_label)




    def display_input_video(self):
        # Check if the user has selected a video
        if not hasattr(self, 'input_video_path') or not self.input_video_path:
            QMessageBox.warning(self,"Aucune vidéo sélectionnée", "Veuillez sélectionner une vidéo avant de continuer.")
            return
            
        # Show interface elements for video processing
        self.crop_widget.show()
        self.reduce_video_button.show()
        self.crop_video_button.show()
        self.draw_line_button.show()
        self.reset_video_button.show()
        self.start_counting_button.show()
        self.cancel_counting_button.show()
        self.first_frame_label.show()

        # Disable crop and draw line until time range is set
        self.crop_video_button.setEnabled(False)
        self.draw_line_button.setEnabled(False)
        
        # Display the input video
        self.display_video(self.input_video_path)


    def setup_time_fields(self):
        # Allow only numbers and ":" with format mm:ss
        validator = QRegularExpressionValidator(QRegularExpression(r"^\d{0,2}:\d{0,2}$"))
        self.start_time_edit.setValidator(validator)
        self.end_time_edit.setValidator(validator)


    def reduce_video(self):
        # Retrieve values from start/end time fields
        start_text = self.start_time_edit.text().strip()
        end_text = self.end_time_edit.text().strip()

        def time_to_seconds(t):
            # Convert 'mm:ss' to total seconds
            if not t or ":" not in t:
                return 0
            try:
                m, s = t.split(":")
                return int(m) * 60 + int(s)
            except:
                return 0

        start_seconds = time_to_seconds(start_text)
        end_seconds = time_to_seconds(end_text)

        # Validate fields: ensure they are filled with valid times
        if start_seconds is None or end_seconds is None:
            QMessageBox.warning(self, "Format invalide", "Veuillez entrer les temps sous la forme mm:ss uniquement avec des chiffres.")
            return

        # Validate timing order: end must be after start
        if end_seconds <= start_seconds:
            QMessageBox.warning(self, "Temps invalide", "Le temps de fin doit être supérieur au temps de début.")
            return
        
        # Ensure times do not exceed total video duration
        if start_seconds > self.total_sec or end_seconds > self.total_sec:
            QMessageBox.warning(self, "Temps hors limites", f"Le temps ne peut pas dépasser la durée totale de la vidéo ({int(self.total_sec)} s).")
            return

        # Store the selected time range for later cropping/export
        self.crop_start_time = start_seconds
        self.crop_end_time = end_seconds

        # Display a confirmation message
        QMessageBox.information(self,"Plage définie",f"La vidéo sera réduite de {start_seconds}s à {end_seconds}s.")

        # Display the first frame for further processing
        self.display_first_frame(self.input_video_path)

        # Enable crop button and disable reduce button after setting the time range
        self.crop_video_button.setEnabled(True)
        self.reduce_video_button.setEnabled(False)


    def crop_video(self):
        # Create an instance of the VideoCropper class, responsible for cropping the video
        crop_drawer = VideoCropper(
            self.first_frame_label,
            self.crop_video_button,
            self.draw_line_button,
            self.input_video_path,
            self.selected_fps,
            self.offset_x,
            self.offset_y,
            self.scale_x,
            self.scale_y,
            self.crop_start_time,
            self.crop_end_time,
            self
        )
        # Store the cropper instance for later use
        self.cropper = crop_drawer

        # Enable cropping functionality
        crop_drawer.enable_crop_video()


    def draw_line(self):
        # If no crop has been done yet, show a warning message
        if self.temp_crop_rect is None:
            QMessageBox.warning(None, "Erreur", "Vous devez d'abord faire un crop.")
            return
        
        # Create an instance of the LineDrawer class to allow drawing a line on the cropped video
        line_drawer = LineDrawer(
            self.first_frame_label,
            self.crop_video_button,
            self.draw_line_button,
            self.input_video_path,
            self.offset_x,
            self.offset_y,
            self.temp_crop_rect,
            self.scale_x,
            self.scale_y,
            self
        )
        # Enable line drawing on the video
        line_drawer.enable_line_drawing()

        # Enable the button to start counting sheep or objects after the line is drawn
        self.start_counting_button.setEnabled(True)
        
        # Connect the button click to the method that crops and exports the video
        self.start_counting_button.clicked.connect(self.cropper.crop_and_export_video)

        # Connect the signal emitted when cropping is done to the sheep detection method  
        self.cropper.crop_done.connect(self.sheep_detector)
      
    
        
    def reset_video(self):
        # Clear any stored data related to cropping and line drawing
        self.line_points = []
        self.video_line_points = []
        self.temp_crop_rect = None
        self.crop_video_path = None
        self.export_path = None

        # Disable line drawing mode
        self.drawing_line = False

        # Remove previously created objects if they exist
        if hasattr(self, 'cropper'):
            self.cropper.deleteLater()
            del self.cropper

        if hasattr(self, 'line_drawer'):
            self.line_drawer.deleteLater()
            del self.line_drawer
        
        # Reset signal connections for the counting button
        try:
            self.start_counting_button.clicked.disconnect()
        except TypeError:
            pass  

        # Remove any existing mouse click event on the first frame label
        self.first_frame_label.mousePressEvent = lambda event: None

        # Re-enable the line drawing and crop buttons
        self.reduce_video_button.setEnabled(True)
        self.start_counting_button.setEnabled(False)

        # Reload the original image 
        self.display_input_video()




    def sheep_detector(self, video_path):
        # Start the loading animation
        self.start_loading()

        def processing():
            detector = SheepDetector(self.model_path) # Initialize the detector
            detector.export_model(self.model_suffix) # Export and load the onnx model
            detector.setup_line_zone(self.video_line_points) # Import the user's line
            detector.setup_annotators() # Set up visual annotators (for drawing boxes, lines, labels, etc.)
            detector.setup_tracking(self.selected_fps) # Update frame rate

            # Run sheep detection on my cropped video and export output video
            self.export_path = detector.run_detection_on_video(video_path)

        class WorkerThread(QThread):
            def run(worker_self):
                processing()
                QTimer.singleShot(0, self._on_detection_done)

        # Instantiate and start the worker thread
        self.worker_thread = WorkerThread()
        self.worker_thread.start()
    

    def _on_detection_done(self):
        self.end_loading() # Stop the loading animation
        self.display_video(self.export_path) # Display the final video with sheep detections


    def start_loading(self):
        self.progress_dialog = QProgressDialog("Comptage en cours...", None, 0, 0) # Create progress dialog
        self.progress_dialog.setWindowTitle("Veuillez patienter") # Set dialog title
        self.progress_dialog.setWindowModality(Qt.WindowModal) # Block interaction with other windows in the app

        self.progress_dialog.setMinimumWidth(400) # Set dialog width
        self.progress_dialog.setMinimumHeight(100) # Set dialog height
        self.progress_dialog.setSizeGripEnabled(True) # Allow manual resizing by the user
        self.progress_dialog.setRange(0, 0) # Set bouncing effect of the progress bar 
        self.progress_dialog.show() # Show the dialog
        QApplication.processEvents() # Force GUI to update immediately


    def end_loading(self):
        self.progress_dialog.close() # Stop the loading animation


    def display_video(self, video_path):
        # Create video output label
        if not hasattr(self, 'media_player'):
            self.media_player = None
            self.video_output = QLabel()
            self.video_output.setScaledContents(False)
            self.video_output.setAlignment(Qt.AlignCenter)  

            # Create control bar overlay (play, pause, stop, time)
            self.controls = QFrame(self.video_output)  
            self.controls.setStyleSheet("""
                QFrame {background-color: rgba(0, 0, 0, 150);}
                QPushButton {color: white; background: transparent; border: none; font-size: 18px;}
            """)
            self.controls.setFixedHeight(50)

            # Control buttons and time display label
            self.play_button = QPushButton("▶", self.controls)
            self.pause_button = QPushButton("⏸", self.controls)
            self.stop_button = QPushButton("⏹", self.controls)
            self.time_label = QLabel("00:00 / 00:00", self.controls)
            self.time_label.setStyleSheet("color: white; font-size: 14px; background-color: transparent;")

            # Layout for the controls
            control_layout = QHBoxLayout(self.controls)
            control_layout.addWidget(self.play_button)
            control_layout.addWidget(self.pause_button)
            control_layout.addWidget(self.stop_button)
            control_layout.addWidget(self.time_label)
            control_layout.setContentsMargins(10, 5, 10, 5)
            self.controls.setLayout(control_layout)

            # Main video container layout
            self.video_container = QWidget()
            video_layout = QVBoxLayout(self.video_container)
            video_layout.addWidget(self.video_output)
            video_layout.setContentsMargins(0, 0, 0, 0)
            self.video_widget.setLayout(QVBoxLayout())
            self.video_widget.layout().addWidget(self.video_container)

            # Connect playback controls
            self.play_button.clicked.connect(lambda: self.set_playback(True))
            self.pause_button.clicked.connect(lambda: self.set_playback(False))
            self.stop_button.clicked.connect(self.stop_video)

            # Timer to refresh video frames
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.video_playing = False

        # If a video is already loaded, reset the player
        if self.media_player:
            self.media_player = None

        # Open the video with ffpyplayer
        self.media_player = MediaPlayer(video_path, ff_opts={'out_fmt': 'rgb24'})
        metadata = self.media_player.get_metadata() or {}
        self.input_fps = float(metadata.get('fps') or 30)
        
        # Position the control overlay at the bottom of the video
        self.controls.setGeometry(
            0,
            self.video_output.height() - self.controls.height(),
            self.video_output.width(),
            self.controls.height()
        )
        self.controls.raise_()  # Ensure it stays above the video display

        # Start playback
        self.video_playing = True
        self.timer.start(int(1000 / self.input_fps))
        self.display_stack.setCurrentWidget(self.video_widget)

        
    def update_frame(self):
        # Do nothing if no media player is active or video is paused
        if not self.media_player or not self.video_playing:
            return

        frame, val = self.media_player.get_frame()

        # Check for end-of-file (EOF) (stop the video properly when the vidéo is done)
        if isinstance(val, str) and "eof" in val:
            self.stop_video()
            return

        if frame is not None:
            # Extract frame data and convert to QPixmap
            img, _ = frame
            w, h = img.get_size()
            data = img.to_bytearray()[0]
            image = QImage(data, w, h, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            # Scale the pixmap to fit the label while keeping the aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.video_output.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.video_output.setPixmap(scaled_pixmap)

            # Reposition the control overlay relative to the scaled video
            video_rect = self.video_output.contentsRect()
            video_height = scaled_pixmap.height()
            video_y = (video_rect.height() - video_height) // 2
            self.controls.move(0, video_y + video_height - self.controls.height())
            self.controls.resize(video_rect.width(), self.controls.height())
            self.controls.raise_()

            # Update playback time display
            pts = self.media_player.get_pts()
            if isinstance(pts, (int, float)): # Avoid errors when EOF is reached
                current_sec = int(pts)
                self.total_sec = int(float(self.media_player.get_metadata().get('duration', 0)))
                
                def sec_to_time(sec):
                    m, s = divmod(sec, 60)
                    return f"{int(m):02}:{int(s):02}"

                self.time_label.setText(f"{sec_to_time(current_sec)} / {sec_to_time(self.total_sec)}")

        # Adjust frame refresh delay dynamically based on playback speed
        if self.video_playing and self.media_player:
            delay = max(int(((val if isinstance(val, (int, float)) else 1/self.input_fps) * 1000)), 1)
            self.timer.start(delay)    


    def set_playback(self, play: bool):
        # Play or pause video
        if self.media_player:
            self.video_playing = play
            self.media_player.set_pause(not play)
            if play and not self.timer.isActive():
                self.timer.start(int(1000 / self.input_fps))
            elif not play:
                self.timer.stop()


    def stop_video(self):
        # Stop video playback and reset to the first frame
        self.video_playing = False
        if self.timer.isActive():
            self.timer.stop()

        if self.media_player:
            try:
                # Pause and seek to the beginning
                self.media_player.set_pause(True)
                self.media_player.seek(0, relative=False)  

                # Fetch and display the first frame after seeking
                frame, _ = self.media_player.get_frame()
                if frame is not None:
                    img, _ = frame
                    w, h = img.get_size()
                    data = img.to_bytearray()[0]
                    image = QImage(data, w, h, QImage.Format_RGB888)
                    self.video_output.setPixmap(QPixmap.fromImage(image))

            except Exception as e:
                print(f"[STOP VIDEO] Erreur : {e}")



    def cancel_counting(self):
        # Clear the list of line points used for drawing
        self.line_points = []
        self.crop_start_time = None
        self.crop_end_time = None


        # Hide the crop, draw line, reset buttons, and first frame
        self.reduce_video_button.hide()
        self.crop_widget.hide()
        self.draw_line_button.hide()
        self.crop_video_button.hide()
        self.reset_video_button.hide()
        self.start_counting_button.hide()
        self.cancel_counting_button.hide()
        self.first_frame_label.hide() 
        self.video_widget.hide()
        

# Launch the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InterfaceApp()
    window.show()
    sys.exit(app.exec_())
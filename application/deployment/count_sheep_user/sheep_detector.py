from ultralytics import YOLO
import supervision as sv
import os
import numpy as np
from datetime import datetime

class SheepDetector:
    def __init__(self, pt_path="models/yolo11n.pt", export_path = "videos/output_videos"):
        # Init molels and export video path
        self.pt_path = pt_path
        self.export_path = export_path
        self.file_name = None
        
        # Load the pytorch model
        self.pytorch_model = YOLO(self.pt_path)
        self.onnx_model = None  

        self.tracker = None
        self.line_zone = None
        self.annotators = {}


    def export_model(self, model_suffix):
        # Build ONNX model path
        self.onnx_path = f"models/yolo{model_suffix}.onnx"  
       
        # Export onnx model if it dosn't exist
        if not os.path.exists(self.onnx_path):
            print("Exporting model to ONNX...")
            self.pytorch_model.export(format="onnx", imgsz=640, simplify=False)
            print(f"Exported to {self.onnx_path}")
        else:
            print("ONNX model already exists.")

        # Load the model
        self.onnx_model = YOLO(self.onnx_path)
    
    
    def setup_line_zone(self, line_points):
        # Create a virtual line for counting
        START = sv.Point(*line_points[0])
        END = sv.Point(*line_points[1])
        print(f"coordonnees recu dans detector: {line_points}")

        self.line_zone = sv.LineZone(start=START, end=END)


    def setup_tracking(self, frame_rate):
        # Set up ByteTrack tracking with custom parameters
        self.tracker = sv.ByteTrack(frame_rate=frame_rate)
        self.lost_track_buffer=60,
        self.tracker.track_activation_threshold = 0.4
        self.tracker.minimum_matching_threshold = 0.7

        # Create the output video file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_file = f"sheep_crossing_{frame_rate}fps_{timestamp}.avi"
        self.export_path = os.path.normpath(os.path.join(self.export_path, video_file))
    

    def setup_annotators(self):
        # Set up visual annotators: bounding box, label, trace, and line counter
        color = sv.ColorPalette.DEFAULT
        color_type = sv.ColorLookup.TRACK

        self.annotators = {
            "box": sv.BoundingBoxAnnotator(thickness=2, color=color, color_lookup=color_type),
            "label": sv.LabelAnnotator(text_thickness=1, text_scale=0.35, text_padding=1),
            "trace": sv.TraceAnnotator(thickness=1),
            "line": sv.LineZoneAnnotator(
                thickness=1, text_thickness=1, text_scale=0.5,
                custom_in_text="in", custom_out_text="out"
            )
        }
    

    def run_detection_on_video(self, video_path):
        # Ensure all components are initialized
        if self.onnx_model is None:
            raise ValueError("ONNX model not loaded. Call export_model() first.")
        if self.tracker is None:
            raise ValueError("Tracker not initialized. Call setup_tracking() first.")
        if not self.line_zone or not self.annotators:
            raise ValueError("Line zone or annotators not set up. Call setup_line_zone() and setup_annotators() first.")

        
        def callback(frame: np.ndarray) -> np.ndarray:
            result = self.onnx_model(frame)[0]
            detection_model = sv.Detections.from_ultralytics(result)
            detections = self.tracker.update_with_detections(detection_model)
            

            labels = [
                f'#{tracker_id} {confidence:0.2f}'
                for tracker_id, confidence in zip(detections.tracker_id, detections.confidence)
            ]

            annotated_frame = self.annotators["box"].annotate(scene=frame.copy(), detections=detections)
            annotated_frame = self.annotators["label"].annotate(annotated_frame, detections, labels)
            annotated_frame = self.annotators["trace"].annotate(annotated_frame, detections=detections)

            self.line_zone.trigger(detections)

            return self.annotators["line"].annotate(annotated_frame, line_counter=self.line_zone)

        video_info = sv.VideoInfo.from_video_path(video_path=video_path)
        frames_generator = sv.get_video_frames_generator(source_path=video_path)

        os.makedirs(os.path.dirname(self.export_path), exist_ok=True)

        with sv.VideoSink(target_path=self.export_path, video_info=video_info) as sink:
            for frame in frames_generator:
                annotated_frame = callback(frame)
                sink.write_frame(frame=annotated_frame)

        return self.export_path
    
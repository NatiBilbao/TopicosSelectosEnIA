from typing import Any
import numpy as np
from ultralytics import YOLO
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "/Users/pepe/dev/upb/topics/ai-topics-2-2023/2.computer_vision_deployment/2.2.training/runs/classify/train12/weights/best.pt"
FACE_MODEL_PATH = "/Users/pepe/dev/upb/topics/ai-topics-2-2023/2.computer_vision_deployment/2.3.trained_models/mediapipe/models/blaze_face_short_range.tflite"

class CatsPredictor:
    def __init__(self, model_path: str = MODEL_PATH):
        print("Creando predictor...")
        self.model = YOLO(model_path)
    
    def predict_file(self, file_path: str):
        results = self.model([file_path])
        pred_data = []
        for i, res in enumerate(results):
            pred_data.append(
                {
                    "category": res.names[res.probs.top1],
                    "confidence":res.probs.data[res.probs.top1].item()
                }
            )
        return pred_data
    
    def predict_image(self, image_array: np.ndarray):
        results = self.model(image_array)[0]

        return {
            "class": results.names[results.probs.top1],
            "confidence": results.probs.data[results.probs.top1].item()
        }
    

class FaceDetector:
    def __init__(self, model_path=FACE_MODEL_PATH):
        # crear modelo
        base_options = python.BaseOptions(model_asset_path=FACE_MODEL_PATH)
        options = vision.FaceDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE
            )
        self.model = vision.FaceDetector.create_from_options(options)
    
    def predict_image(self, image_array: np.ndarray):
        # convertir array de numpy a formato compatible
        mp_image= mp.Image(image_format=mp.ImageFormat.SRGB, data=image_array)
        detection = self.model.detect(mp_image)
        results = []
        for detection in detection.detections:
            bbox = detection.bounding_box
            detection_dict = {
                "bbox": [bbox.origin_x, bbox.origin_y, bbox.width, bbox.height],
                "keypoints": [(kp.x, kp.y) for kp in detection.keypoints]
            }
            results.append(detection_dict)
        return results


if __name__ == "__main__":
    image_file = "/Users/pepe/dev/upb/topics/ai-topics-2-2023/2.computer_vision_deployment/2.3.trained_models/mediapipe/person.jpg"
    img = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2RGB)
    predictor = FaceDetector()
    prediction = predictor.predict_image(img)
    print(prediction)


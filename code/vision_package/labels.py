from enum import Enum


labels_yolo = {'person': 0, 'bicycle': 1, 'car': 2, 'motorcycle': 3, 'airplane': 4, 'bus': 5, 'train': 6, 'truck': 7,
              'boat': 8, 'traffic light': 9, 'fire hydrant': 10, 'stop sign': 11, 'parking meter': 12, 'bench': 13,
              'bird': 14, 'cat': 15, 'dog': 16, 'horse': 17, 'sheep': 18, 'cow': 19, 'elephant': 20, 'bear': 21,
              'zebra': 22, 'giraffe': 23, 'backpack': 24, 'umbrella': 25, 'handbag': 26, 'tie': 27, 'suitcase': 28,
              'frisbee': 29, 'skis': 30, 'snowboard': 31, 'sports ball': 32, 'kite': 33, 'baseball bat': 34,
              'baseball glove': 35, 'skateboard': 36, 'surfboard': 37, 'tennis racket': 38, 'bottle': 39,
              'wine glass': 40, 'cup': 41, 'fork': 42, 'knife': 43, 'spoon': 44, 'bowl': 45, 'banana': 46, 'apple': 47,
              'sandwich': 48, 'orange': 49, 'broccoli': 50, 'carrot': 51, 'hot dog': 52, 'pizza': 53, 'donut': 54,
              'cake': 55, 'chair': 56, 'couch': 57, 'potted plant': 58, 'bed': 59, 'dining table': 60, 'toilet': 61,
              'tv': 62, 'laptop': 63, 'mouse': 64, 'remote': 65, 'keyboard': 66, 'cell phone': 67, 'microwave': 68,
              'oven': 69, 'toaster': 70, 'sink': 71, 'refrigerator': 72, 'book': 73, 'clock': 74, 'vase': 75,
               'scissors': 76, 'teddy bear': 77, 'hair drier': 78, 'toothbrush': 79,
                'background':80
               }


class RiskLevel(Enum):
    VERY_HIGH = 100
    HIGH = 80
    MEDIUM = 60
    LOW = 40
    ZERO = 0

risk_table = {
    "person": RiskLevel.VERY_HIGH,
    "bicycle": RiskLevel.VERY_HIGH,
    "car": RiskLevel.VERY_HIGH,
    "motorcycle": RiskLevel.VERY_HIGH,
    "airplane": RiskLevel.VERY_HIGH,
    "bus": RiskLevel.VERY_HIGH,
    "train": RiskLevel.VERY_HIGH,
    "truck": RiskLevel.VERY_HIGH,
    "boat": RiskLevel.VERY_HIGH,
    "traffic light": RiskLevel.MEDIUM,
    "fire hydrant": RiskLevel.MEDIUM,
    "stop sign": RiskLevel.MEDIUM,
    "parking meter": RiskLevel.MEDIUM,
    "bench": RiskLevel.MEDIUM,
    "bird": RiskLevel.MEDIUM,
    "cat": RiskLevel.MEDIUM,
    "dog": RiskLevel.MEDIUM,
    "horse": RiskLevel.MEDIUM,
    "sheep": RiskLevel.MEDIUM,
    "cow": RiskLevel.MEDIUM,
    "elephant": RiskLevel.MEDIUM,
    "bear": RiskLevel.MEDIUM,
    "zebra": RiskLevel.MEDIUM,
    "giraffe": RiskLevel.MEDIUM,
    "backpack": RiskLevel.MEDIUM,
    "umbrella": RiskLevel.MEDIUM,
    "handbag": RiskLevel.MEDIUM,
    "tie": RiskLevel.MEDIUM,
    "suitcase": RiskLevel.MEDIUM,
    "frisbee": RiskLevel.MEDIUM,
    "skis": RiskLevel.MEDIUM,
    "snowboard": RiskLevel.MEDIUM,
    "sports ball": RiskLevel.MEDIUM,
    "kite": RiskLevel.MEDIUM,
    "baseball bat": RiskLevel.MEDIUM,
    "baseball glove": RiskLevel.MEDIUM,
    "skateboard": RiskLevel.MEDIUM,
    "surfboard": RiskLevel.MEDIUM,
    "tennis racket": RiskLevel.MEDIUM,
    "bottle": RiskLevel.VERY_HIGH,
    "wine glass": RiskLevel.HIGH,
    "cup": RiskLevel.HIGH,
    "fork": RiskLevel.LOW,
    "knife": RiskLevel.LOW,
    "spoon": RiskLevel.LOW,
    "bowl": RiskLevel.MEDIUM,
    "banana": RiskLevel.MEDIUM,
    "apple": RiskLevel.HIGH,
    "sandwich": RiskLevel.MEDIUM,
    "orange": RiskLevel.HIGH,
    "broccoli": RiskLevel.MEDIUM,
    "carrot": RiskLevel.MEDIUM,
    "hot dog": RiskLevel.MEDIUM,
    "pizza": RiskLevel.MEDIUM,
    "donut": RiskLevel.MEDIUM,
    "cake": RiskLevel.MEDIUM,
    "chair": RiskLevel.MEDIUM,
    "couch": RiskLevel.MEDIUM,
    "potted plant": RiskLevel.MEDIUM,
    "bed": RiskLevel.MEDIUM,
    "dining table": RiskLevel.MEDIUM,
    "toilet": RiskLevel.MEDIUM,
    "tv": RiskLevel.MEDIUM,
    "laptop": RiskLevel.MEDIUM,
    "mouse": RiskLevel.MEDIUM,
    "remote": RiskLevel.LOW,
    "keyboard": RiskLevel.LOW,
    "cell phone": RiskLevel.MEDIUM,
    "microwave": RiskLevel.MEDIUM,
    "oven": RiskLevel.MEDIUM,
    "toaster": RiskLevel.MEDIUM,
    "sink": RiskLevel.MEDIUM,
    "refrigerator": RiskLevel.MEDIUM,
    "book": RiskLevel.LOW,
    "clock": RiskLevel.MEDIUM,
    "vase": RiskLevel.MEDIUM,
    "scissors": RiskLevel.MEDIUM,
    "teddy bear": RiskLevel.MEDIUM,
    "hair drier": RiskLevel.MEDIUM,
    "toothbrush": RiskLevel.LOW,
    "background": RiskLevel.ZERO,
}

if __name__ == "__main__":
    print(labels_yolo)
    print(risk_table["toothbrush"].value)
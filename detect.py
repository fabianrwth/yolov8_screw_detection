from ultralytics import YOLO
import os

model_path = os.path.join(".", "runs", "detect", "train7", "weights", "best.pt")

# Load a model
model = YOLO(model_path)  # load a custom model
model.conf = 0.2  # set confidence threshold

# Predict with the model
model.predict("example.jpg", show=True)


# val_results = model.val()

# with open("val_results.txt", "w") as f:
#     f.write(str(val_results))

from ultralytics import YOLO
import os

model_path = os.path.join(".", "runs", "detect", "train11", "weights", "best.pt")

# Load a model
model = YOLO(model_path)  # load a custom model
model.conf = 0.2  # set confidence threshold

# Validate model
val_results = model.val()

# Save validation results
with open("val_results.txt", "w") as f:
    f.write(str(val_results))

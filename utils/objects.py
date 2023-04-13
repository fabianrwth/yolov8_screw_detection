import torch


def load_model(weights="yolov5s", conf=0.25, iou=0.45):


    model = torch.hub.load(source, weights)

    return model

def check_model(weights):
    
from roboflow import Roboflow

rf = Roboflow(api_key="mmGNEBdkdjiTGgNWRuQR")
project = rf.workspace("cse-jnn70").project("fastener-5eskb")
dataset = project.version(1).download("yolov8")

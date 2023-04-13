import cv2
import numpy as np
import os
import json

import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


def hands_detect(img):
    mp_hands = mp.solutions.hands
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
        input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input_img = cv2.flip(input_img, 1)  # horizontal flip
        results = hands.process(input_img)
        handedness = results.multi_handedness
        hands_coordinates = results.multi_hand_landmarks

    return handedness, hands_coordinates


# flip x coordinates, necessary because of the mediapipe output format
def flip_xcoords(hands_coordinates):
    coords = []

    for idx in range(len(hands_coordinates)):
        hand_landmarks = hands_coordinates[idx].landmark
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend(
            [landmark_pb2.NormalizedLandmark(x=1 - landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks]
        )
        coords.append(hand_landmarks_proto)

    return coords


def hands_label(handedness):
    handedness_list = []
    for i in handedness:
        handedness_list.append(i.classification[0].label.lower())

    return handedness_list  # ['left', 'right']


def draw_landmarks(rgb_image, hands_label, hands_coordinates):

    MARGIN = 20  # pixels
    FONT_SIZE = 2
    FONT_THICKNESS = 2
    HANDEDNESS_TEXT_COLOR = [(88, 205, 54), (28, 28, 236)]

    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hands_coordinates)):
        hand_landmarks = hands_coordinates[idx].landmark
        handedness = hands_label[idx]

        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            hands_coordinates[idx],
            solutions.hands.HAND_CONNECTIONS,
            solutions.drawing_styles.get_default_hand_landmarks_style(),
            solutions.drawing_styles.get_default_hand_connections_style(),
        )

        # Get the top left corner of the detected hand's bounding box.
        height, width, _ = annotated_image.shape
        x_coordinates = [landmark.x for landmark in hand_landmarks]
        y_coordinates = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coordinates) * width)
        text_y = int(min(y_coordinates) * height) - MARGIN

        # Draw handedness (left or right hand) on the image.
        cv2.putText(
            annotated_image,
            f"{handedness}",
            (text_x, text_y),
            cv2.FONT_HERSHEY_DUPLEX,
            FONT_SIZE,
            HANDEDNESS_TEXT_COLOR[idx],
            FONT_THICKNESS,
            cv2.LINE_AA,
        )

    # annotated_image = cv2.flip(annotated_image, 1)
    return annotated_image


# save hands information in json format
def hands_json(handedness, hands_coordinates, file_name="output_hands.json", file_path="./"):

    FILE_PATH = os.path.join(file_path, file_name)

    coords = dict()
    for i in range(len(hands_coordinates)):
        temp_handedness = handedness[i]
        coords[temp_handedness] = {}
        for j, landmark in enumerate(hands_coordinates[i].landmark):
            coords[temp_handedness][j] = {
                "x": hands_coordinates[i].landmark[j].x,
                "y": hands_coordinates[i].landmark[j].y,
                "z": hands_coordinates[i].landmark[j].z,
            }

    with open(FILE_PATH, "w") as f:
        json.dump(coords, f, indent=4, sort_keys=True)

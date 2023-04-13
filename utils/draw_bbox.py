"""
Draws bounding boxes on an image based on annotations.

Usage: 
$ python draw_bbox.py --image_path <path_to_image> --annotations_path <path_to_annotations> [-m] [-c] [-s]

Required arguments:
    --image_path:   Path to the input image.
    --annotations_path: Path to the annotations file.

Optional arguments:
    -m, --draw_markers: Whether to draw center markers on the bounding boxes. Default: False.
    -c, --show_class: Whether to show class labels next to the boxes. Default: False.
    -s, --save_image: Whether to save the output image. Default: False.
"""

import cv2
import argparse


def draw_bbox(image_path, annotations_path, draw_markers=False, save_image=False, show_class=False):

    """
    Draws bounding boxes on an image based on annotations.

    Args:
        image_path (str): Path to the input image.
        annotations_path (str): Path to the annotations file.
        draw_markers (bool): Whether to draw center markers on the bounding boxes (default: False).
        save_image (bool): Whether to save the output image (default: False).
        show_class (bool): Whether to show class labels (default: False).
    """
    # Load the image
    img = cv2.imread(image_path)
    height = float(img.shape[0])
    width = float(img.shape[1])

    print(draw_markers, save_image, show_class)
    # Load annotations
    with open(annotations_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            class_idx, x_center, y_center, bbox_width, bbox_height = line.split()

            # Convert the YOLO format bounding box to (xmin, ymin, xmax, ymax) format
            xmin = (float(x_center) - (float(bbox_width) / 2)) * width
            ymin = (float(y_center) - (float(bbox_height) / 2)) * height
            xmax = (float(x_center) + (float(bbox_width) / 2)) * width
            ymax = (float(y_center) + (float(bbox_height) / 2)) * height

            # Draw the bounding box on the image
            cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 255), thickness=4)

            if draw_markers:
                # Draw the center point of the bounding box on the image
                center_x = int(float(x_center) * width)
                center_y = int(float(y_center) * height)
                cv2.drawMarker(img, (center_x, center_y), markerType=1, markerSize=20, color=(0, 0, 255), thickness=2)

            # Add the category label next to the box
            if show_class:
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.2
                label = "{}".format(class_idx)
                cv2.putText(
                    img, label, (int(xmin) + 5, int(ymin) + 20), font, font_scale, (20, 20, 20), thickness=2, lineType=cv2.LINE_AA
                )

            # print(f"CENTER: {x_center}, {y_center}")

    # Show the image
    cv2.imshow("image", cv2.resize(img, None, fx=0.5, fy=0.5))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if save_image:
        cv2.imwrite("output.jpg", cv2.resize(img, None, fx=0.5, fy=0.5))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw bounding boxes on an image.")
    parser.add_argument("--image_path", required=True, type=str, help="path to the input image")
    parser.add_argument("--annotations_path", required=True, type=str, help="path to the annotations file")
    parser.add_argument("-m", "--draw_markers", action="store_true", help="turn on/off drawing of center markers (default: on)")
    parser.add_argument("-c", "--show_class", action="store_true", help="turn on/off showing class labels (default: on)")
    parser.add_argument("-s", "--save_image", action="store_true", help="turn on/off saving the output image (default: off)")
    args = parser.parse_args()
    print(args)
    draw_bbox(args.image_path, args.annotations_path, args.draw_markers, args.save_image, args.show_class)

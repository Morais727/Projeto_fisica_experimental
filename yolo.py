import os
import shutil
import cv2
import numpy as np
from ultralytics import YOLO

def detect_bananas(image_path):
    """Detect bananas in the image and return their bounding boxes."""
    model = YOLO('yolov8n.pt')  # Load YOLOv8 Small model
    results = model(image_path)
    img = cv2.imread(image_path)
    bananas = []

    for result in results[0].boxes.data.cpu().numpy():
        x1, y1, x2, y2, conf, cls = result
        if int(cls) == 46:  # Class 46 is 'banana' in COCO dataset
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cropped_banana = img[y1:y2, x1:x2]
            bananas.append((cropped_banana, (x1, y1, x2, y2)))

    return bananas

def analyze_curvature(banana_img):
    """Analyze the curvature of the banana to determine its orientation."""
    # Convert to grayscale and apply binary threshold
    gray = cv2.cvtColor(banana_img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get the largest contour (assumes it's the banana)
        contour = max(contours, key=cv2.contourArea)

        # Fit a polynomial (2nd degree) to the contour points
        points = np.squeeze(contour)
        if len(points) < 5:  # Not enough points to fit a curve
            return "Unknown"

        # Fit a parabola to the contour
        fit = np.polyfit(points[:, 0], points[:, 1], 2)  # y = ax^2 + bx + c

        # Check the sign of the quadratic coefficient (a)
        curvature = fit[0]
        if curvature > 0:
            return "Concave Down"
        elif curvature < 0:
            return "Concave Up"
        else:
            return "Flat"

    return "Unknown"

def process_folder_and_organize(folder_path, output_folder_up, output_folder_down):
    """Process all images in a folder and organize them by banana orientation."""
    if not os.path.exists(output_folder_up):
        os.makedirs(output_folder_up)
    if not os.path.exists(output_folder_down):
        os.makedirs(output_folder_down)

    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if not image_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        bananas = detect_bananas(image_path)
        orientations = [analyze_curvature(banana_img) for banana_img, _ in bananas]

        # Determine dominant orientation
        concave_up_count = orientations.count("Concave Up")
        concave_down_count = orientations.count("Concave Down")

        if concave_up_count > concave_down_count:
            destination = os.path.join(output_folder_up, image_name)
            shutil.copy(image_path, destination)
            print(f"Copied {image_name} to Concave Up folder")
        elif concave_down_count > concave_up_count:
            destination = os.path.join(output_folder_down, image_name)
            shutil.copy(image_path, destination)
            print(f"Copied {image_name} to Concave Down folder")
        else:
            print(f"Skipping {image_name}: Unable to determine dominant orientation")

# Main program
folder_path = 'EXP_FISICA_imagens_experimento'
output_folder_up = 'output_folder/concave_up'  # Folder for Concave Up images
output_folder_down = 'output_folder/concave_down'  # Folder for Concave Down images

process_folder_and_organize(folder_path, output_folder_up, output_folder_down)

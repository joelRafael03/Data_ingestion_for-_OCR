import os
import pathlib
import transformers #type: ignore
import json
import numpy as np
import cv2 
import easyocr #type: ignore



# Paths
PATH_TO_IMAGES = pathlib.Path(
    "./images/sample/"
)
TEMP_PATH = pathlib.Path(
    "temp/"
)
TEMP_PATH.mkdir(parents=True, exist_ok=True)

if not PATH_TO_IMAGES.exists():
    raise FileNotFoundError(
        f"{PATH_TO_IMAGES} not found."
    )

# Result dictionary
all_results = {}

# Loop through the images
for image_path in PATH_TO_IMAGES.iterdir():

    # Skip directories
    if not image_path.is_file():
        continue

    # Only process image files
    if image_path.suffix.lower() not in [
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    ]:
        continue

    print(f"Processing: {image_path.name}")

    # Run OCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext("images/3.jpg")
    
    for res in result:
        print(f"Text: {res[1]}, Coordinates: {res[0]}")

    image = cv2.imread("images/3.jpg")
    # Loop through each detection
    for bbox, text, prob in result:

        if prob < 0.6:
            continue

        # Extract top-left and bottom-right points or polygon coordinates
        pts = np.array(bbox, dtype=np.int32)

        # Reshape for contour/polylines drawing
        pts = pts.reshape((-1, 1, 2))

        # Draw a multi-point polygon bounding box
        cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Put the detected text above the bounding box
        # top_left = tuple(bbox[0])
        cv2.putText(
            image,
            text,
            #(top_left[0], top_left[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )

# Save or display the result image
cv2.imwrite('output_image.jpg', image)
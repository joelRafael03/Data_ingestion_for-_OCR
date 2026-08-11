import json
import pathlib

import paddleocr
from paddleocr import PaddleOCR

from schemas import OCRLine, OCRPage


# -----------------------------
# Versions
# -----------------------------

print(f"PaddleOCR version: {paddleocr.__version__}")

import transformers
print(f"Transformers version: {transformers.__version__}")


# -----------------------------
# Paths
# -----------------------------

PATH_TO_IMAGES = pathlib.Path(
    "/Users/sutantojoel/060826/images"
)

TEMP_PATH = pathlib.Path(
    "/Users/sutantojoel/060826/temp"
)

TEMP_PATH.mkdir(parents=True, exist_ok=True)


if not PATH_TO_IMAGES.exists():
    raise FileNotFoundError(
        f"{PATH_TO_IMAGES} not found."
    )


# -----------------------------
# Initialize PaddleOCR
# -----------------------------

ocr = PaddleOCR(
    use_doc_orientation_classify=True,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle",
)


# -----------------------------
# Master Dictionary
# -----------------------------

all_results = {}


# -----------------------------
# Loop Through Images
# -----------------------------

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


    # -----------------------------
    # Run OCR
    # -----------------------------

    results = ocr.predict(str(image_path))


    # -----------------------------
    # Save temporary PaddleOCR JSON
    # -----------------------------

    json_path = TEMP_PATH / "temp.json"

    for result in results:
        result.save_to_json(
            save_path=json_path
        )


    # -----------------------------
    # Load PaddleOCR JSON
    # -----------------------------

    with open(json_path, "r") as j:
        data = json.load(j)


    # -----------------------------
    # Add to Master Dictionary
    # -----------------------------

    all_results[image_path.name] = {
        "image_path": str(image_path),
        "rec_texts": data["rec_texts"]
    }


# -----------------------------
# Save Final JSON
# -----------------------------

OUTPUT_PATH = TEMP_PATH / "all_ocr_results.json"

with open(OUTPUT_PATH, "w") as f:
    json.dump(
        all_results,
        f,
        indent=4
    )


# -----------------------------
# Print Final Result
# -----------------------------

print("\nFinal JSON:")
print(json.dumps(all_results, indent=4))

print(f"\nSaved to: {OUTPUT_PATH}")
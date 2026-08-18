import json
from datasets import Dataset

ANNOTATIONS = "structured_output/new_file.json"
OUTPUT = "data/raw"


# Load annotations
with open(ANNOTATIONS, "r", encoding="utf-8") as f:
    annotations = json.load(f)


# Convert dictionary → list of rows
samples = []

for filename, data in annotations.items():

    samples.append({
        "image": data["image_path"],
        "fields": data["fields"]
    })


# Create Hugging Face Dataset
dataset = Dataset.from_list(samples)

print(dataset)

# Save
dataset.save_to_disk(OUTPUT)

print(f"Saved dataset to {OUTPUT}")

import json
import pathlib

IMAGE_PATH = pathlib.Path("images/")
JSON_PATH = pathlib.Path("structured_output/output.json")
OUTPUT_PATH = pathlib.Path("images_renamed/")
OUTPUT_PATH.mkdir(exist_ok=True)

# Load JSON
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = {}

for i, (old_name, item) in enumerate(data.items(), start=1):

    # Get extension from original filename
    suffix = pathlib.Path(old_name).suffix.lower()

    # New filename
    new_name = f"image{i}{suffix}"

    # Old and new image paths
    old_path = IMAGE_PATH / old_name
    new_path = OUTPUT_PATH / new_name

    # Rename physical image
    if old_path.exists():
        old_path.rename(new_path)
    else:
        print(f"WARNING: Image not found: {old_path}")

    # Update image_path
    item["image_path"] = str(new_path.resolve())

    # Add under new filename
    new_data[new_name] = item


# Save updated JSON
with open(JSON_PATH, "w") as f:
    json.dump(new_data, f, indent=4)

print("Done!")


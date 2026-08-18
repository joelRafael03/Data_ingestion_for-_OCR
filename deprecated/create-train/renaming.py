
import json
import pathlib

IMAGE_PATH = pathlib.Path("images/")
JSON_PATH = pathlib.Path("structured_output/output.json")

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
    new_path = IMAGE_PATH / new_name

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
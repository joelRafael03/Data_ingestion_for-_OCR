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
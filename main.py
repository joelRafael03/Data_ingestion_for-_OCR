import json
from pathlib import Path

from llm import process_ocr


# ============================================================
# Paths
# ============================================================

INPUT_FILE = Path(
    "/Users/sutantojoel/060826/temp/all_ocr_results.json"
)

OUTPUT_DIR = Path(
    "/Users/sutantojoel/060826/structured_output"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = OUTPUT_DIR / "output.json"


# ============================================================
# Load OCR JSON
# ============================================================

with INPUT_FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)


print(f"Found {len(data)} images.")
print()


# ============================================================
# Process each image
# ============================================================

output = {}

for index, (image_name, image_data) in enumerate(
    data.items(),
    start=1
):

    print(
        f"[{index}/{len(data)}] Processing {image_name}",
        flush=True
    )

    # Send ONLY the current image to the LLM
    result = process_ocr({
        image_name: image_data
    })

    # Convert LLM JSON string → Python dictionary
    result_dict = json.loads(result)

    # Add result to master dictionary
    output.update(result_dict)


# ============================================================
# Save Final JSON
# ============================================================

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(
        output,
        f,
        indent=4,
        ensure_ascii=False
    )


# ============================================================
# Done
# ============================================================

print()
print("=" * 60)
print("LLM PROCESSING COMPLETE")
print("=" * 60)
print(f"Images processed: {len(output)}")
print(f"Output saved to: {OUTPUT_FILE}")
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import random
import io

# ============================================================
# PATHS
# ============================================================

BASE = Path("/Users/sutantojoel/060826/mykad_dataset")

INPUT_IMAGES = BASE / "train/images"
INPUT_LABELS = BASE / "train/labels"

OUTPUT_IMAGES = BASE / "train/images_augmented"
OUTPUT_LABELS = BASE / "train/labels_augmented"

OUTPUT_IMAGES.mkdir(parents=True, exist_ok=True)
OUTPUT_LABELS.mkdir(parents=True, exist_ok=True)

# Reproducible randomness
random.seed(42)
np.random.seed(42)


# ============================================================
# BLUR
# ============================================================

def add_blur(image):

    radius = random.uniform(0.5, 2.0)

    return image.filter(
        ImageFilter.GaussianBlur(radius)
    )


# ============================================================
# SHADOW
# ============================================================

def add_shadow(image):

    image = image.convert("RGB")

    width, height = image.size

    arr = np.array(image).astype(np.float32)

    # Random shadow region
    x1 = random.randint(0, int(width * 0.5))
    y1 = random.randint(0, int(height * 0.5))

    x2 = random.randint(
        int(width * 0.5),
        width
    )

    y2 = random.randint(
        int(height * 0.5),
        height
    )

    mask = np.zeros(
        (height, width),
        dtype=np.uint8
    )

    mask[y1:y2, x1:x2] = 255

    shadow = Image.fromarray(mask)

    # Soft shadow edges
    shadow = shadow.filter(
        ImageFilter.GaussianBlur(
            random.uniform(15, 40)
        )
    )

    mask = (
        np.array(shadow).astype(np.float32)
        / 255.0
    )

    darkness = random.uniform(
        0.20,
        0.50
    )

    arr *= (
        1 - mask[:, :, None] * darkness
    )

    arr = np.clip(
        arr,
        0,
        255
    ).astype(np.uint8)

    return Image.fromarray(arr)


# ============================================================
# LIGHTING
# ============================================================

def change_lighting(image):

    # Brightness
    brightness = random.uniform(
        0.70,
        1.30
    )

    image = ImageEnhance.Brightness(
        image
    ).enhance(brightness)

    # Contrast
    contrast = random.uniform(
        0.80,
        1.25
    )

    image = ImageEnhance.Contrast(
        image
    ).enhance(contrast)

    # Slight saturation change
    saturation = random.uniform(
        0.85,
        1.15
    )

    image = ImageEnhance.Color(
        image
    ).enhance(saturation)

    return image


# ============================================================
# CAMERA QUALITY
# ============================================================

def change_camera_quality(image):

    width, height = image.size

    # Simulate lower resolution camera
    scale = random.uniform(
        0.55,
        0.85
    )

    small_size = (
        max(32, int(width * scale)),
        max(32, int(height * scale))
    )

    image = image.resize(
        small_size,
        Image.Resampling.BILINEAR
    )

    # Restore original dimensions
    image = image.resize(
        (width, height),
        Image.Resampling.BILINEAR
    )

    # Sensor noise
    arr = np.array(
        image
    ).astype(np.float32)

    noise_strength = random.uniform(
        2,
        8
    )

    noise = np.random.normal(
        0,
        noise_strength,
        arr.shape
    )

    arr += noise

    arr = np.clip(
        arr,
        0,
        255
    ).astype(np.uint8)

    image = Image.fromarray(arr)

    # JPEG compression
    quality = random.randint(
        40,
        85
    )

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=quality
    )

    buffer.seek(0)

    return Image.open(
        buffer
    ).convert("RGB")


# ============================================================
# RANDOM COMBINATION
# ============================================================

def combined(image):

    operations = [
        add_blur,
        add_shadow,
        change_lighting,
        change_camera_quality
    ]

    random.shuffle(operations)

    # Apply 2-4 effects
    number = random.randint(2, 4)

    for operation in operations[:number]:
        image = operation(image)

    return image


# ============================================================
# COPY LABEL
# ============================================================

def copy_label(
    original_label,
    new_label
):

    if not original_label.exists():

        print(
            f"WARNING: Missing label "
            f"{original_label.name}"
        )

        return False

    new_label.write_text(
        original_label.read_text()
    )

    return True


# ============================================================
# MAIN
# ============================================================

extensions = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}

images = [
    p for p in INPUT_IMAGES.iterdir()
    if p.suffix.lower() in extensions
]

print(
    f"Found {len(images)} training images."
)

augmentation_functions = [
    ("blur", add_blur),
    ("shadow", add_shadow),
    ("lighting", change_lighting),
    ("camera", change_camera_quality),
    ("combined", combined)
]

total = 0

for index, image_path in enumerate(images):

    print(
        f"[{index + 1}/{len(images)}] "
        f"{image_path.name}"
    )

    label_path = (
        INPUT_LABELS /
        f"{image_path.stem}.txt"
    )

    original = Image.open(
        image_path
    ).convert("RGB")

    for name, function in augmentation_functions:

        augmented = function(
            original.copy()
        )

        output_name = (
            f"{image_path.stem}_{name}.jpg"
        )

        output_image = (
            OUTPUT_IMAGES /
            output_name
        )

        output_label = (
            OUTPUT_LABELS /
            f"{image_path.stem}_{name}.txt"
        )

        augmented.save(
            output_image,
            format="JPEG",
            quality=90
        )

        if copy_label(
            label_path,
            output_label
        ):
            total += 1


print()
print("==============================")
print("AUGMENTATION COMPLETE")
print("==============================")
print(
    f"Original training images: "
    f"{len(images)}"
)
print(
    f"Augmented images created: "
    f"{total}"
)
print(
    f"Output images: "
    f"{OUTPUT_IMAGES}"
)
print(
    f"Output labels: "
    f"{OUTPUT_LABELS}"
)
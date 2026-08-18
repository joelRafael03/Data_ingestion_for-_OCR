from ultralytics import YOLO

model = YOLO(
    "/Users/sutantojoel/060826/runs/detect/train/weights/best.pt"
)

metrics = model.val(
    data="My First Project.v1i.yolo26 2/data.yaml",
    split="train"
)

print(metrics)
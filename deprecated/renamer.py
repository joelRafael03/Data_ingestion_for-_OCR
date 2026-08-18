import os

input_folder = "images_renamed"
output_folder= "rename"

for i, old_name in enumerate(os.listdir(input_folder)):
    old_path = os.path.join(input_folder, old_name)
    new_path = os.path.join(output_folder, f"myKad{i}.jpg")
    os.rename(old_path, new_path)
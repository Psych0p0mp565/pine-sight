import os
import json
from PIL import Image
from pathlib import Path
from collections import defaultdict
import pandas as pd

# Folder where YOLO saves predictions
predict_dir = Path("runs/detect/predict")

# Prepare a report dictionary
report = defaultdict(list)

# Loop through all txt detection files
for txt_file in predict_dir.glob("labels/*.txt"):
    image_name = txt_file.stem + ".jpg"  # assuming original file was .jpg
    with open(txt_file, "r") as file:
        detections = file.readlines()
        report["Image Name"].append(image_name)
        report["Detection Count"].append(len(detections))

# Convert to DataFrame
df = pd.DataFrame(report)

# Save to CSV for easy sharing
report_path = "detection_report.csv"
df.to_csv(report_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="YOLOv8 Detection Report", dataframe=df)
report_path

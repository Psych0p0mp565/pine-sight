from ultralytics import YOLO
import cv2
import os

# Load your model
model = YOLO("best.pt")

# Ask user for the image filename
image_name = input("Enter the image filename (inside test_images/ folder): ")

# Paths
image_folder = "test_images"
image_path = os.path.join(image_folder, image_name)

# Check if image exists
if not os.path.exists(image_path):
    print(f"❌ Error: {image_path} does not exist.")
    exit()

print(f"🔍 Running detection on {image_name}...")

# Run YOLOv8 detection
results = model(image_path, save=True)

# Print detections info
for result in results:
    print("\n📋 Detection Results:")
    if result.boxes is not None:
        for i, box in enumerate(result.boxes):
            cls_id = int(box.cls[0])
            class_name = result.names[cls_id]
            confidence = float(box.conf[0])
            coords = box.xyxy[0].tolist()
            print(f"#{i+1} - {class_name} ({confidence:.2f}) at {coords}")
    else:
        print("No detections found.")

# Find latest runs/detect/predict*/ output
runs_dir = "runs/detect"
subdirs = sorted([d for d in os.listdir(runs_dir) if d.startswith("predict")], reverse=True)
latest_predict = os.path.join(runs_dir, subdirs[0])
output_path = os.path.join(latest_predict, image_name)

# Show result image
if os.path.exists(output_path):
    img = cv2.imread(output_path)
    if img is not None:
        cv2.imshow(f"Detected: {image_name}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"❌ Failed to open detected image: {output_path}")
else:
    print(f"❌ Detection output not found: {output_path}")

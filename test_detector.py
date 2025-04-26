from ultralytics import YOLO
import cv2
import os

# Load your model
model = YOLO("best.pt")

# Folder with test images
image_folder = "test_images"

# Run detection on each image
for image_name in os.listdir(image_folder):
    if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(image_folder, image_name)
        print(f"🔍 Running detection on {image_name}...")

        # Run YOLOv8
        results = model(image_path, save=True)

        # Show the result image
        output_path = f"runs/detect/predict/{image_name}"
        img = cv2.imread(output_path)
        if img is not None:
            cv2.imshow(f"Detected: {image_name}", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"Failed to open result: {output_path}")

# main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import torch

app = FastAPI()

# Enable CORS (so your mobile app can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained YOLOv8 model
model = YOLO("model/best.pt")  # make sure best.pt is here

@app.get("/")
async def root():
    return {"message": "Pine-Sight backend is running!"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    results = model(image)[0]  # run detection
    detections = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(float, box.xyxy[0])
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        detections.append({
            "class": class_name,
            "confidence": round(confidence, 2),
            "box": [x1, y1, x2, y2]
        })

    return {"detections": detections}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


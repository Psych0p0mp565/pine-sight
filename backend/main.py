from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io

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
model = YOLO("model/best.pt")  # Make sure best.pt is in model/
print("✅ YOLO model loaded!")

@app.get("/")
async def root():
    return {"message": "Pine-Sight backend is running!"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    print(f"📥 Received file: {file.filename}")

    # Validate image content type
    if file.content_type not in ["image/jpeg", "image/png"]:
        print(f"❗ Unsupported file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Unsupported image type")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Run detection
        results = model(image)[0]
        detections = []

        confidence_threshold = 0.5

        for box in results.boxes:
            confidence = float(box.conf[0])
            if confidence < confidence_threshold:
                continue

            x1, y1, x2, y2 = map(float, box.xyxy[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            detections.append({
                "class": class_name,
                "confidence": round(confidence, 2),
                "box": [x1, y1, x2, y2]
            })

        print(f"📦 Detections returned: {detections}")
        return {"detections": detections}

    except Exception as e:
        print(f"❌ Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Image processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

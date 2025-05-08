# 🍍 Pine-Sight

Pine-Sight is a mobile AI-powered detection system that uses YOLOv8 and geospatial technology to identify mealybug infestations in pineapple plants. It integrates a React Native frontend (via Expo) with a FastAPI backend to provide real-time pest detection and mapping support for farmers.

---

## 📱 Features

- 🧠 **YOLOv8-based object detection** for identifying mealybugs in pineapple plant images.
- 📲 **React Native mobile app** (Expo) for real-time photo capture and detection.
- 🌐 **FastAPI backend** serving YOLOv8 model for image analysis.
- 📡 **Ngrok tunnel support** for mobile-backend connectivity.
- 🗺️ (Coming Soon) Geotagging and mapping of pest hotspots.
- 🖼️ (Coming Soon) Visualization of bounding boxes on detected insects.

---

## 🛠 Technologies Used

| Component         | Stack                     |
|------------------|---------------------------|
| Mobile Frontend  | React Native + Expo       |
| Backend API      | Python + FastAPI + Uvicorn|
| Object Detection | YOLOv8 (Ultralytics)      |
| Image Handling   | expo-image-picker         |
| Dev Tools        | ngrok, Git, VSCode        |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js + npm
- Expo CLI
- Ngrok (for public backend access)

---

### 🔧 Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

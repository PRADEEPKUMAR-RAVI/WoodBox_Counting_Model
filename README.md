# 📦 YOLO Wood Box Counter  

This project demonstrates a FastAPI-based application that detects and counts stacked wooden boxes in images using a custom-trained **YOLOv8 model**.  

## 🧠 Model  

The model was trained on wooden box images and fine-tuned with **YOLOv8** for accurate object detection.  

## 📦 Features  

- Detects and counts stacked wooden boxes in uploaded images  
- Returns the number of boxes detected  
- Provides an annotated image with bounding boxes  
- Simple FastAPI endpoints for health check, prediction, and annotated image retrieval  

## 🚀 How to Use  

1. Clone the project and navigate to the directory.  
2. Install dependencies:  

```bash
pip install -r requirements.txt


Run the FastAPI app:

uvicorn app:app --reload


Open your browser at http://127.0.0.1:8000/docs to test the API.
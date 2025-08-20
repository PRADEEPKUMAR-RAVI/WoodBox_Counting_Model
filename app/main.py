from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from ultralytics import YOLO
import cv2
import numpy as np
import shutil
import os
from tempfile import NamedTemporaryFile

model = YOLO("/home/softsuave/Downloads/best.pt") 

app = FastAPI(title="YOLO Wood Box Counter")


@app.get("/health/")
async def get_health():
    try:
        return {"health": "ok"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        suffix = os.path.splitext(file.filename)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
    finally:
        file.file.close()

    # Verify file is readable
    img = cv2.imread(temp_path)
    if img is None:
        os.remove(temp_path)
        return {"error": "Uploaded file is not a valid image."}

    # Run YOLO
    results = model(temp_path)
    num_boxes = len(results[0].boxes)

    # Draw only bounding boxes (no labels, no confidence)
    for box in results[0].boxes.xyxy:  # xyxy format: [x1, y1, x2, y2]
        x1, y1, x2, y2 = map(int, box[:4])
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # green boxes

    # Save annotated image
    annotated_path = temp_path.replace(suffix, f"_annotated{suffix}")
    cv2.imwrite(annotated_path, img)

    # Cleanup uploaded file
    os.remove(temp_path)

    # Return annotated image with JSON metadata
    return JSONResponse(content={
        "file_name": file.filename,
        "stacked_wood_boxes": num_boxes,
        "annotated_image": f"/annotated/{os.path.basename(annotated_path)}"
    })


# Serve annotated images
@app.get("/annotated/{filename}")
async def get_annotated(filename: str):
    file_path = f"/tmp/{filename}"  # adjust path if needed
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg")
    return {"error": "File not found"}



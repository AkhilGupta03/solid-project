import os
import cv2
import numpy as np
from PIL import Image

# Update paths as needed
trainimage_path = "TrainingImage"
haar_path = "haarcascade_frontalface_default.xml"
model_path = "TrainingImageLabel/Trainner.yml"

# Load Haar cascade and trained model
detector = cv2.CascadeClassifier(haar_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(model_path)
 

image_paths = []
labels = []
 
# Collect image paths and expected labels
for folder in os.listdir(trainimage_path):
    folder_path = os.path.join(trainimage_path, folder)
    if os.path.isdir(folder_path):
        for img_file in os.listdir(folder_path):
            image_paths.append(os.path.join(folder_path, img_file))
            labels.append(int(folder.split("_")[0]))

correct = 0
total = len(image_paths)
confidence_values = []

# Predict and compare with actual labels
for idx, image_path in enumerate(image_paths):
    img = Image.open(image_path).convert("L")
    img_np = np.array(img, "uint8")
    id_actual = labels[idx]
    faces = detector.detectMultiScale(img_np)
    for (x, y, w, h) in faces:
        id_pred, conf = recognizer.predict(img_np[y:y + h, x:x + w])
        confidence_values.append(conf)
        if id_pred == id_actual and conf < 70:
            correct += 1
        break  # Assume one face per image

accuracy = (correct / total) * 100 if total > 0 else 0
avg_conf = sum(confidence_values) / len(confidence_values) if confidence_values else 0

print(f"Total Images Tested: {total}")
print(f"Correct Recognitions: {correct}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"Average Confidence: {avg_conf:.2f}")

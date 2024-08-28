import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import os

# Initialize Streamlit app
st.title("SnitchGuard - Real-time Face Recognition")

# Sidebar for settings
st.sidebar.title("Settings")
model_name = st.sidebar.selectbox("Choose Face Recognition Model", ["VGG-Face", "Facenet", "OpenFace", "DeepID", "Dlib"])

# Placeholder for displaying video
frame_window = st.image([])

# Access the webcam (0 is the default webcam)
cap = cv2.VideoCapture(0)

# Function to detect and recognize faces
def detect_faces(frame, authorized_faces_encodings):
    # Convert frame to RGB (OpenCV uses BGR by default)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        # DeepFace verification to identify faces
        result = DeepFace.find(img_path=rgb_frame, db_path="authorised_faces", model_name=model_name, enforce_detection=False)
        return result
    except Exception as e:
        st.error(f"Error in face recognition: {e}")
        return None

# Load authorized faces into memory (optional: replace with your own authorized faces folder)
authorized_faces_folder = "authorised_faces"
if not os.path.exists(authorized_faces_folder):
    os.makedirs(authorized_faces_folder)

authorized_faces_encodings = {}

# Process video frames from the webcam
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to read from webcam.")
        break
    
    # Display the current frame
    frame_window.image(frame, channels="BGR")

    # Perform face recognition
    result = detect_faces(frame, authorized_faces_encodings)

    # Display result
    if result:
        st.write("Unauthorized access detected!" if len(result) > 0 else "Access granted.")

    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

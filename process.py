import streamlit as st
import cv2
import face_recognition
import numpy as np
from twilio.rest import Client
import os

# Load authorized faces
def load_and_encode_faces(folder_path='authorised_faces'):
    encoded_faces = []
    face_names = []

    for file_name in os.listdir(folder_path):
        image = face_recognition.load_image_file(os.path.join(folder_path, file_name))
        encoding = face_recognition.face_encodings(image)[0]
        encoded_faces.append(encoding)
        face_names.append(os.path.splitext(file_name)[0])

    return encoded_faces, face_names

encoded_faces, face_names = load_and_encode_faces()

def identify_faces(encoded_faces, face_names):
    st.title("SnitchGuard: AI-Powered Security System")
    
    # Start capturing from the webcam
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Detect faces and find encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Check if faces are recognized
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(encoded_faces, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(encoded_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = face_names[best_match_index]
            else:
                send_whatsapp_notification()

            # Display results
            st.write(f"Detected: {name}")

        # Display the resulting frame in Streamlit
        st.image(frame, channels="BGR")

    video_capture.release()
    cv2.destroyAllWindows()

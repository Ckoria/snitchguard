import streamlit as st
import cv2
import numpy as np
import face_recognition
import os
from report import write_to_csv
from notification import send_sms

def read_authorised_faces(path: str) -> list:
    """Reads all files in the selected directory."""
    return os.listdir(path)

def convert_img_colors(authorised_faces: list) -> list:
    """Converts images from BGR to RGB for processing."""
    processed_images = [cv2.cvtColor(cv2.imread(f'./authorised_faces/{face}'), cv2.COLOR_BGR2RGB)
                        for face in authorised_faces]
    return processed_images

def encode_images(processed_images: list) -> list:
    """Encodes processed images."""
    encoded_images = []
    for img in processed_images:
        encodings = face_recognition.face_encodings(img)
        if encodings:  # Only add if a face encoding was found
            encoded_images.append(encodings[0])  # Append the first encoding found
    return encoded_images

def image_names(authorised_faces: list) -> list:
    """Extracts names from image files."""
    return [face.split(".")[0] for face in authorised_faces]

def match_faces(face_frame, face_encodes, encoded_images, image) -> None:
    """Matches faces from a list of authorized faces."""
    for encode_face, face_loc in zip(face_encodes, face_frame):
        match = face_recognition.compare_faces(encoded_images, encode_face)
        face_distance = face_recognition.face_distance(encoded_images, encode_face)
        match_name(face_distance, match, face_loc, image)

def match_name(face_distance, match, face_loc, image):
    """Identifies and labels the best match for detected faces."""
    match_idx = np.argmin(face_distance)
    authorised_faces = read_authorised_faces("authorised_faces")
    authorised_names = image_names(authorised_faces)
    
    if match[match_idx]:
        name = authorised_names[match_idx].title()
        draw_rectangle(image, face_loc, name, True)
    else:
        name = 'UNKNOWN'
        draw_rectangle(image, face_loc, name, False)
        send_sms()

    write_to_csv(name)
    st.image(image, channels="RGB")

def draw_rectangle(image, face_loc, name, authorized):
    """Draws rectangles and labels around detected faces."""
    y1, x2, y2, x1 = face_loc
    color = (0, 255, 0) if authorized else (255, 0, 0)
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    cv2.rectangle(image, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
    cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

def start_face_recognition(encoded_images) -> None:
    """Handles the webcam feed and performs face recognition."""
    camera_on = cv2.VideoCapture(0)

    # Place the stop button outside the loop
    stop_button = st.button("Stop", key="stop_button")
    
    while camera_on.isOpened():
        ret, image = camera_on.read()
        if not ret:
            st.warning("Failed to access the webcam.")
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_frame = face_recognition.face_locations(image)
        face_encodes = face_recognition.face_encodings(image, face_frame)

        if face_encodes:
            match_faces(face_frame, face_encodes, encoded_images, image)
        else:
            st.image(image, channels="RGB")

        # Check the stop button to break the loop
        if stop_button:
            camera_on.release()
            cv2.destroyAllWindows()
            break

def main():
    st.title("Face Recognition App")
    st.write("This app uses your webcam to perform face recognition in real-time.")

    if st.button("Start Face Recognition", key="start_button"):
        authorised_faces = read_authorised_faces("authorised_faces")
        processed_images = convert_img_colors(authorised_faces)
        encoded_images = encode_images(processed_images)

        start_face_recognition(encoded_images)

if __name__ == "__main__":
    main()

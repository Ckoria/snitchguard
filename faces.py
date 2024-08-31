import cv2
import numpy as np
import face_recognition
import os
from report import write_to_csv
from notification import send_sms

def read_authorised_faces(path: str) -> list:
    """
        Takes the path and read all files in a directory
    Args:
        path (str): Selected directory
    Returns:
        list : Files in a selected directory
    """
    return os.listdir(path)


def convert_img_colors(authorised_faces: list) -> list:
    """
        - Convert images color from BGR to RGB for openCV processesing
    Args:
        list : authorised_faces   
    Returns:
        list : Processed images with corrected color 
    """
    # authorised_faces = read_authorised_faces('authorised_faces')
    # Returns list comprehension of converted colors
    processed_images = [cv2.cvtColor(cv2.imread(
            f'./authorised_faces/{face}'), cv2.COLOR_BGR2RGB)
        for face in authorised_faces ]
    return processed_images 


def encode_images(processed_images: list) -> list:
    """
     - Encode processed images
    Args:
        list : processed images
    Returns:
      list : Encoded processed images
    """
    # Flatten the list of face encodings
    encoded_images = []
    for img in processed_images:
        encodings = face_recognition.face_encodings(img)
        if encodings:  # Only add if a face encoding was found
            encoded_images.append(encodings[0])  # Append the first encoding found
    return encoded_images
    
    
def image_names(authorised_faces: list) -> list:
    """
        - Get names from images
    Args:
        list : authorised_faces
    Returns:
        list: image names
    """
    return [face.split(".")[0] for face in authorised_faces]


def read_camera(camera_on, encoded_images) -> None:
    """
     - Reads live images on a camera and finds a match from a list of authorised faces
    """ 
    if camera_on.isOpened():
        success, image = camera_on.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(success)
        face_frame = face_recognition.face_locations(image)
        face_encodes = face_recognition.face_encodings(image, face_frame)  
        print(face_encodes)
        match_faces(face_frame, face_encodes, encoded_images, image)
        

def match_faces(face_frame, face_encodes, encoded_images, image) -> None:
    """
    - Matches faces from a list of authorised faces
    Args:
        face_frame (_type_): frame around detected face
        face_encodes (_type_): encoded face
    """
    for encode_face, face_loc in zip(face_encodes, face_frame):
        match = face_recognition.compare_faces(encoded_images, encode_face)
        face_distance = face_recognition.face_distance(encoded_images, encode_face)
        print(face_distance)
        match_name(face_distance, match, face_loc, image)
  
        
def match_name(face_distance, match, face_loc, image):
    """
        - Grab the best match 
    Args:
        face_distance (list): 
        match (list): matching values
        face_loc (tuple): 
        image (cv): image from a camera
    """
    match_idx = np.argmin(face_distance)
    authorised_faces = read_authorised_faces("authorised_faces")
    authorised_names = image_names(authorised_faces)
    print(match)
    print(match_idx)
    if match[match_idx]:
        name = authorised_names[match_idx].title()
        y1, x2, y2, x1 = face_loc
        cv2.rectangle(image, (x1, y1), (x2, y2),(0,255,0),2)
        cv2.rectangle(image, (x1, y2-35), (x2, y2),(0,255,0), cv2.FILLED)
        cv2.putText(image, name,(x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,255), 2)
    else:
        name = 'UNKOWN'
        y1, x2, y2, x1 = face_loc
        cv2.rectangle(image, (x1, y1), (x2, y2),(255,0,0),2)
        cv2.rectangle(image, (x1, y2-35), (x2, y2),(255,0,0), cv2.FILLED) # Name tag
        cv2.putText(image, name,(x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
        send_sms()
    
    write_to_csv(name)
    cv2.imshow('Webcam', image)
    cv2.waitKey(1)
    
        
        

        
    
    
    
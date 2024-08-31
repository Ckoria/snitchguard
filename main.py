from faces import *
import cv2

if __name__ == "__main__":
    authorised_faces = read_authorised_faces("authorised_faces")
    processed_images = convert_img_colors(authorised_faces)
    encoded_images = encode_images(processed_images)
    camera_on = cv2.VideoCapture(0)
    while True:
        read_camera(camera_on, encoded_images)
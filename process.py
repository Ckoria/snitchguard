import cv2
from deepface import DeepFace
from twilio.rest import Client
import time
from notification import send_whatsapp_notification
# Load authorized images and create embeddings
authorized_faces = ["authorised_faces/IMG_20240323_154409.jpg", 
                    "authorised_faces/IMG_20240308_144954.jpg", 
                    "authorised_faces/IMG_20220924_202946.jpg"]
authorized_embeddings = []

for face in authorized_faces:
    embedding = DeepFace.represent(face, model_name='VGG-Face')
    authorized_embeddings.append(embedding)

# Function to check if the face is authorized
def is_authorized_face(frame):
    try:
        # Get embedding for current frame face
        result = DeepFace.find(frame, db_path="authorised_faces/", model_name='VGG-Face')
        return len(result) > 0  # Return True if face is found in the database
    except Exception as e:
        print(f"Error in face recognition: {e}")
        return False

# Initialize webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Perform face recognition
    authorized = is_authorized_face(frame)
    
    # If the face is not authorized, send a notification
    if not authorized:
        print("Unauthorized face detected!")
        # Call notification function
        # send_whatsapp_notification()
        # Wait for some time before checking again to avoid spam
        time.sleep(10)

    # Display the frame
    cv2.imshow("Webcam", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

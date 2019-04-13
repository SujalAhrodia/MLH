
import glob
import os
import logging
import face_recognition
import cv2
import numpy as np


IMAGES_PATH = './images'  # put your reference images in here
CAMERA_DEVICE_ID = 0
MAX_DISTANCE = 0.5 # increase to make recognition less strict, decrease to make more strict

def get_face_embeddings_from_image(image, convert_to_rgb=False):
    """
    Take a raw image and run both the face detection and face embedding model on it
    """
    # Convert from BGR to RGB if needed
    if convert_to_rgb:
        image = image[:, :, ::-1]

    # run the face detection model to find face locations
    face_locations = face_recognition.face_locations(image)

    # run the embedding model to get face embeddings for the supplied locations
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_locations, face_encodings

def setup_database():
    """
    Load reference images and create a database of their face encodings
    """
    database = {}

    for filename in glob.glob(os.path.join(IMAGES_PATH, '*.jpg')):
        # load image
        image_rgb = face_recognition.load_image_file(filename)
        # use the name in the filename as the identity key
        identity = os.path.splitext(os.path.basename(filename))[0]
        # get the face encoding and link it to the identity
        locations, encodings = get_face_embeddings_from_image(image_rgb)
        database[identity] = encodings[0]

    return database


def paint_detected_face_on_image(frame, location, name=None):
    """
    Paint a rectangle around the face and write the name
    """
    # unpack the coordinates from the location tuple
    top, right, bottom, left = location

    if name is None:
        name = 'Unknown'
        color = (0, 0, 255)  # red for unrecognized face
    else:
        color = (0, 128, 0)  # dark green for recognized face

    # Draw a box around the face
    cv2.rectangle(frame, (left,top), (right, bottom), color, 2)
    
    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
    cv2.putText(frame, name, (left + 6, bottom - 6),
                                cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)




def run_face_recognition(database):
    """
    Start the face recognition via the webcam
    """
    video_capture = cv2.VideoCapture(0)
    known_face_encodings = list(database.values())
    known_face_names = list(database.keys())

    while video_capture.isOpened():
        ok, frame = video_capture.read()
        if not ok:
            logging.error("Could not read frame from camera. Stopping video capture.")
            break

        face_locations, face_encodings = get_face_embeddings_from_image(frame, convert_to_rgb=True)

        print(len(face_locations))
        if len(face_locations)==1 :
            for location, face_encoding in zip(face_locations, face_encodings):

                distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                if np.any(distances <= MAX_DISTANCE):
                    # send to API for successful login
                    flag = True 
                    best_match_idx = np.argmin(distances)
                    name = known_face_names[best_match_idx]
                else:
                    name = None
                    #send API call for sign up

                paint_detected_face_on_image(frame, location, name)
        else:
            # cv2.putText(frame,'Please move one person out of the frame!!',(10,500), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255),2,cv2.LINE_AA)
            # send api for msg 
            flag = False

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

database = setup_database()
run_face_recognition(database)

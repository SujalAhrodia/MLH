
import glob
import os
import logging
import face_recognition
import cv2
import dlib
import numpy as np
import imutils
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import time

IMAGES_PATH = './static/people'  # put your reference images in here
CAMERA_DEVICE_ID = 0
MAX_DISTANCE = 0.5 # increase to make recognition less strict, decrease to make more strict
BLINK_THRSH= 1.10


def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) **2 / (2.0 * C)

	# return the eye aspect ratio
	return ear

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

    #finding features of a face
    face_landmarks = face_recognition.face_landmarks(image)

    return face_locations, face_encodings, face_landmarks

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
        locations, encodings, landmarks = get_face_embeddings_from_image(image_rgb)
        database[identity] = encodings[0]

    return database

database = setup_database()

known_face_encodings = list(database.values())
known_face_names = list(database.keys())

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FPS, 60)

    def __del__(self):
        self.video.release()
    
    def run_face_recognition(self):
        ok, frame = self.video.read()
        name = None
        frame = imutils.resize(frame, width=512)

        face_locations, face_encodings, face_landmarks = get_face_embeddings_from_image(frame, convert_to_rgb=True)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if len(face_locations)==1 :
            for location, face_encoding, landmarks in zip(face_locations, face_encodings, face_landmarks):

                distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                # print(face_landmarks[0]['left_eye'])

                left = eye_aspect_ratio(face_landmarks[0]['left_eye'])
                right = eye_aspect_ratio(face_landmarks[0]['right_eye'])

                EAR = (left+right)/2.0

                # print(EAR)
                # print(face_locations[0][0], face_locations[0][1], face_locations[0][2],)

                if np.any(distances <= MAX_DISTANCE):
                    best_match_idx = np.argmin(distances)
                    name = known_face_names[best_match_idx]
                    if EAR < BLINK_THRSH:
                        # send to API for successful login
                        flag = True 
                        print("Gotcha!")
                        cv2.putText(frame,'BLINK',(100,100), cv2.FONT_HERSHEY_DUPLEX, 1,(255),2,cv2.LINE_AA)
                    # print(name)
                else:
                    name = None
                    #send API call for sign up
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                paint_detected_face_on_image(frame, location, name)
        else:
            cv2.putText(frame,'Please move one person out of the frame!!',(10,500), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255),2,cv2.LINE_AA)
            # send api for msg 
            flag = False
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), name

# VideoCamera()

import mediapipe as mp
from mediapipe import solutions
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import time
import math

# Function to draw landmarks on an image.
def draw_landmarks_on_image(rgb_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)

    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        # Draw the face landmarks.
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
        ])

        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles
            .get_default_face_mesh_tesselation_style())
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles
            .get_default_face_mesh_contours_style())
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles
            .get_default_face_mesh_iris_connections_style())

    return annotated_image

# Constant
MOUTH_AR_THRESHOLD = 0.75  # Threshold for detecting yawning

"""
# Function to compute aspect ratio for eye
def eye_aspect_ratio(landmarks, upper_indices, lower_indices):
    upper_eye = np.mean([[landmarks[i].x, landmarks[i].y] for i in upper_indices], axis=0)
    lower_eye = np.mean([[landmarks[i].x, landmarks[i].y] for i in lower_indices], axis=0)
    vertical = np.linalg.norm(upper_eye - lower_eye)
    if vertical < 1:
        return True
    else:
        return False
"""

# Function to compute aspect ratio for mouth (for yawning detection)
def mouth_aspect_ratio(landmarks, upper_lip, lower_lip):
    vertical = np.linalg.norm(np.array([landmarks[upper_lip[3]].x, landmarks[upper_lip[3]].y]) -
                              np.array([landmarks[lower_lip[7]].x, landmarks[lower_lip[7]].y]))
    horizontal = np.linalg.norm(np.array([landmarks[upper_lip[0]].x, landmarks[lower_lip[0]].x]) -
                                np.array([landmarks[upper_lip[-1]].x, landmarks[lower_lip[-1]].x]))
    
    mar = vertical / horizontal
    return mar

# Indices for left and right eyes and mouth landmarks
#RIGHT_EYE_UPPER = [246, 161, 160, 159, 158, 157, 173]  # rightEyeUpper0
#RIGHT_EYE_LOWER = [33, 7, 163, 144, 145, 153, 154]  # rightEyeLower0
#LEFT_EYE_UPPER = [466, 388, 387, 386, 385, 384, 398]  # leftEyeUpper0
#LEFT_EYE_LOWER = [263, 249, 390, 373, 374, 380, 381]  # leftEyeLower0
MOUTH_UPPER = [61, 185, 40, 39, 37, 0, 267, 269, 270]  # lipsUpperOuter
MOUTH_LOWER = [146, 91, 181, 84, 17, 314, 405, 321]  # lipsLowerOuter

# Create a FaceLandmarker object with the model.
base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# Initialize variable for eye closed detection
eye_closed_time = 0
eye_conf = []

# Initialize variables for yawn detection
yawn_start_time = 0
yawining = False
yawn_conf = []

# Capture video from webcam.
cap = cv2.VideoCapture(2)

# Check if the webcam is opened correctly.
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert the image to RGB format required by MediaPipe.
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # Detect face landmarks.
    detection_result = detector.detect(mp_image)
    face_landmarks_list = detection_result.face_landmarks

    if face_landmarks_list:
        # Use the first detected face
        face_landmarks = face_landmarks_list[0]
        
        # Correct the way to access landmarks
        landmarks = face_landmarks  # face_landmarks_list is already a list of landmarks

        # Eye aspect ratios (EAR) for both eyes
        #left_ear = eye_aspect_ratio(landmarks, LEFT_EYE_UPPER, LEFT_EYE_LOWER)
        #right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE_UPPER, RIGHT_EYE_LOWER)
        left_eye = math.sqrt(math.pow(landmarks[159].x-landmarks[145].x,2) + math.pow(landmarks[159].y-landmarks[145].y,2))
        right_eye = math.sqrt(math.pow(landmarks[386].x-landmarks[374].x,2) + math.pow(landmarks[374].y-landmarks[477].y,2))

        # Mouth aspect ratio (MAR) for yawning detection
        mar = mouth_aspect_ratio(landmarks, MOUTH_UPPER, MOUTH_LOWER)

        # Detect yawning.
        if (mar > MOUTH_AR_THRESHOLD and left_eye<1 and right_eye<1):
            if (eye_closed_time != 0 and time.time() - eye_closed_time > 1):
                if not yawning:
                    yawn_start_time = time.time()
                yawning = True
                yawn_conf.append(True)
        else:
            yawning = False
            if (yawn_start_time != 0 and len(yawn_conf) > 30 and time.time() - yawn_start_time > 6):
                print("Yawning was detected; Consider taking a break or going to bed!")
                yawn_start_time = 0
                yawn_conf.clear()
                eye_conf.clear()

        # Detect eye closure for 5 seconds (30 fps)
        if left_eye < 1 and right_eye < 1:
            if eye_closed_time == 0:
                eye_closed_time = time.time()
                eye_conf.clear()
            elif len(eye_conf) < 150:
                eye_conf.append(True)
            elif len(eye_conf)==150:
                print("Eye closure was detected; Consider getting some rest!")
                eye_conf.clear()
        else:
            eye_closed_time = 0
            eye_conf.clear()
            
    # Display the image with landmarks
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    annotated_image = draw_landmarks_on_image(rgb_image, detection_result)
    cv2.imshow('Face Landmarks', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close 
cap.release()
cv2.destroyAllWindows()

import mediapipe as mp
import cv2
import math
from playsound import playsound
import time

mp_face_detection = mp.solutions.face_detection

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_drawing_styles = mp.solutions.drawing_styles

mp_pose = mp.solutions.pose

embarrasment = 0
screenStreak = time.time()
screentime = 600 # seconds
blinks = [0, time.time()]
eyeState = [True, True]

def punish(reason):
    global embarrasment
    # playsound('I Want To Be Ninja! (Neenja) Original song by Jennifer Murphy.mp3')
    print(reason)

def vzn():
    global screenStreak, embarrasment, blinks
    cap = cv2.VideoCapture(0)
    faces = mp
    face = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        refine_landmarks=True,
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    )
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1, 
        min_detection_confidence=0.5
    )
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rFaces = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = face.process(rgb_frame)
        if rFaces.detections:
            if time.time()-screenStreak>screentime:
                punish('too long')
        else:
            screenStreak = time.time()
        
        if blinks[0]>=8:
            punish('eye bad')
        if blinks[0]==0:
            blinks[1]=time.time()
        else:
            blinks[0] = max(0, blinks[0]-(5*(time.time()-blinks[1])))
            blinks[1]=time.time()

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                height, width, _ = frame.shape
                dx = face_landmarks.landmark[469].x - face_landmarks.landmark[471].x
                dx *= width
                dX = 11.7
                normalizedFocaleX = 1.5
                fx = min(height, width) * normalizedFocaleX
                dZ = (fx * (dX / dx))/10.0
                if dZ<50:
                    punish('too close')
                rightEye = face_landmarks.landmark[159].y-face_landmarks.landmark[145].y
                leftEye = face_landmarks.landmark[386].y-face_landmarks.landmark[374].y
                if -0.01<leftEye<0.01 and eyeState[0] and dZ<100:
                    blinks[0]+=1
                    eyeState[0]=False
                else:
                    eyeState[0]=True
                if -0.01<rightEye<0.01 and eyeState[1] and dZ<100:
                    blinks[0]+=1
                    eyeState[1]=False
                else:
                    eyeState[1]=True
                mp_drawing.draw_landmarks(
                    image=rgb_frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=rgb_frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=rgb_frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
        cv2.imshow('MediaPipe Face Mesh', cv2.flip(rgb_frame, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

vzn()
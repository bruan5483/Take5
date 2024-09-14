import mediapipe as mp
import cv2
import math
from playsound import playsound
import time
import numpy as np

jumping_punishment = False

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

counter = 0
stage = None 
cap = None

pose = mp_pose.Pose(
    min_detection_confidence = 0.5, min_tracking_confidence = 0.5
)

# Function to calculate angle
def calculate_angle(a,b,c):
    a = np.array(a) #First
    b = np.array(b) #Mid
    c = np.array(c) #End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0])-np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle>180.0:
        angle=360-angle
    
    return angle

def jumping():
    global counter, mp_pose, cap
    while counter<5:
        image = cap.read()[1]
        results = pose.process(image)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            shoulder1=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip1=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            wrist1=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            ankle1=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            shoulder2=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            hip2=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            wrist2=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            ankle2=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # Calculate angle
            angle1 = calculate_angle(hip1, shoulder1, wrist1)
            angle2 = calculate_angle(hip2, shoulder2, wrist2)
            angle3 = calculate_angle(shoulder1, hip1, ankle1)
            angle4 = calculate_angle(shoulder2, hip2, ankle2)

            if angle1 < 30 and angle2 < 30 and angle3 > 170 and angle4 > 170 :
                stage = 'down'
            if angle1 > 160 and angle2 > 160 and angle3 < 160 and angle4 < 160 and stage == 'down':
                stage = 'up'
                counter+=1
        else:
            pass

def punish(reason):
    global jumping_punishment
    # playsound('I Want To Be Ninja! (Neenja) Original song by Jennifer Murphy.mp3')
    # print(reason)
    jumping_punishment = True


def vzn():
    global screenStreak, embarrasment, blinks, cap, jumping_punishment, counter
    cap = cv2.VideoCapture(0)
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
            
        if jumping_punishment:
            image1 = cap.read()[1]
            results1 = pose.process(image1)
            if results1.pose_landmarks:
                landmarks = results1.pose_landmarks.landmark

                # Get coordinates
                shoulder1=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip1=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                wrist1=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                ankle1=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                shoulder2=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                hip2=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                wrist2=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                ankle2=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                # Calculate angle
                angle1 = calculate_angle(hip1, shoulder1, wrist1)
                angle2 = calculate_angle(hip2, shoulder2, wrist2)
                angle3 = calculate_angle(shoulder1, hip1, ankle1)
                angle4 = calculate_angle(shoulder2, hip2, ankle2)

                if angle1 < 30 and angle2 < 30 and angle3 > 170 and angle4 > 170 :
                    stage = 'down'
                if angle1 > 160 and angle2 > 160 and angle3 < 160 and angle4 < 160 and stage == 'down':
                    stage = 'up'
                    counter+=1
                    print(counter)
            else:
                pass
            mp_drawing.draw_landmarks(image1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                )
            if counter>=5:
                jumping_punishment = False
                counter = 0
                stage = None
        else:
            print('garbage')
            rFaces = face_detection.process(frame)
            results = face.process(frame)
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
                    if dZ<40:
                        punish('too close')
                    rightEye = face_landmarks.landmark[159].y-face_landmarks.landmark[145].y
                    leftEye = face_landmarks.landmark[386].y-face_landmarks.landmark[374].y
                    if -0.009<leftEye<0.009 and eyeState[0] and dZ<100:
                        blinks[0]+=1
                        eyeState[0]=False
                    else:
                        eyeState[0]=True
                    if -0.009<rightEye<0.009 and eyeState[1] and dZ<100:
                        blinks[0]+=1
                        eyeState[1]=False
                    else:
                        eyeState[1]=True
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())
            cv2.imshow('MediaPipe Face Mesh', cv2.flip(frame, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

vzn()
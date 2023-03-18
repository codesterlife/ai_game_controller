import mediapipe as mp
import numpy as np
import cv2
import pyautogui
import time

jumpThresh = 80
prevHeight = 0
newHeight = 0
KeyAlreadyDown = False
KeyAlreadyUp = True
pressSpace = False
startt = 0
endt = 0

def inFrameCheck(LandmarkList):
    if (LandmarkList[0].visibility > 0.7) and (LandmarkList[19].visibility > 0.7):
        return True
    return False

def sumall(LandmarkList):
    sum = 0
    for i in LandmarkList:
        sum += (i.y * 480)

    return sum

def checkJump(LandmarkList):
    if LandmarkList[0].y * 480 < jumpThresh:
        return True
    return False

def pcycle(v):
    global arr
    for i in reversed(range(1, arr.shape[0])):
        arr[i] = arr[i - 1]

    arr[0] = v

def sumofdiff():
    global arr

    sum = 0
    for i in arr:
        sum += i

    return sum


arr = np.zeros((10))
pose = mp.solutions.pose
drawing = mp.solutions.drawing_utils
poseC = pose.Pose()
cap = cv2.VideoCapture(0)

stime = time.time()
etime = time.time()

while True:
    stime = time.time()

    success, frame = cap.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.blur(frame, (5, 5))
    cv2.line(frame, (0, jumpThresh), (640, jumpThresh), (255, 0, 0), 2)
    res = poseC.process(rgb)

    drawing.draw_landmarks(frame, res.pose_landmarks, pose.POSE_CONNECTIONS)

    if res:
        if inFrameCheck(res.pose_landmarks.landmark):
            
            newHeight = sumall(res.pose_landmarks.landmark)

            pcycle(abs(newHeight - prevHeight))

            if (sumofdiff()) > 400:
                if not(KeyAlreadyDown):
                    pyautogui.keyDown('d')
                    print("key down")
                    KeyAlreadyDown = True
                    KeyAlreadyUp = False

            else:
                if not (KeyAlreadyUp):
                    pyautogui.keyUp('d')
                    print("key up")
                    KeyAlreadyUp = True
                    KeyAlreadyDown = False


            prevHeight = newHeight


            if checkJump(res.pose_landmarks.landmark) and not (pressSpace):
                print("jump")
                pressSpace = True
                startt = time.time()
                pyautogui.keyDown("space")

            if pressSpace:
                endt = time.time()
                if(endt - startt) > 0.5:
                    pyautogui.keyUp("space")
                    pressSpace = False

        else:
            cv2.putText(frame, "Out of Frame!", (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


    etime = time.time()
    cv2.putText(frame, str(int(1 / (etime - stime))), (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("window", frame)

    if cv2.waitKey(1) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
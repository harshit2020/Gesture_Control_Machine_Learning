import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import distance as d
import numpy as np
import pyautogui


ccap = cv2.VideoCapture(0)
mmpHand = mp.solutions.hands
hand_func = mmpHand.Hands()
mmpDraws = mp.solutions.drawing_utils
dev = AudioUtilities.GetSpeakers()

iface = dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
adjvolume = cast(iface, POINTER(IAudioEndpointVolume))

MinVol, MaxVol = adjvolume.GetVolumeRange()[:2]

left_click = False
right_click = False
swipe_start = None
pyautogui.FAILSAFE = False
alt_key_pressed = False
horizontal_swipe_threshold = 60  # Adjust this threshold as needed
# Get the screen resolution
screen_width, screen_height = pyautogui.size()

# Calculate the scaling factor between webcam and screen coordinates
webcam_width, webcam_height = ccap.get(cv2.CAP_PROP_FRAME_WIDTH), ccap.get(cv2.CAP_PROP_FRAME_HEIGHT)
x_scale = (screen_width / webcam_width)*1.7
y_scale = (screen_height / webcam_height)*1.7

landmarks_list = []

while True:
    ssess, frame_img = ccap.read()
    RGB_image = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)
    frame_result = hand_func.process(RGB_image)
    List_landmark = []
    if frame_result.multi_hand_landmarks:
        for hand_landmarks in frame_result.multi_hand_landmarks:
            for id_mark, hand_mark in enumerate(hand_landmarks.landmark):
                height_frame, width_frame, c = frame_img.shape
                current_x, current_y = int(hand_mark.x * width_frame), int(hand_mark.y * height_frame)
                List_landmark.append([id_mark, current_x, current_y])

            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * frame_img.shape[1])
                y = int(landmark.y * frame_img.shape[0])
                landmarks_list.append((x, y))

            mmpDraws.draw_landmarks(frame_img, hand_landmarks, mmpHand.HAND_CONNECTIONS)
            if List_landmark != []:
                coor_x1, coor_y1 = List_landmark[4][1], List_landmark[4][2]  # Thumb
                coor_x5, coor_y5 = List_landmark[8][1], List_landmark[8][2]  # Index finger
                coor_x17, coor_y17 = List_landmark[20][1], List_landmark[20][2]  # Little finger

            cv2.circle(frame_img, (coor_x1, coor_y1), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame_img, (coor_x5, coor_y5), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame_img, (coor_x17, coor_y17), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(frame_img, (coor_x1, coor_y1), (coor_x5, coor_y5), (255, 0, 0), 3)  # Line from thumb to index finger
            cv2.line(frame_img, (coor_x1, coor_y1), (coor_x17, coor_y17), (255, 0, 0), 3)  # Line from thumb to little finger
            length = hypot(coor_x5 - coor_x1, coor_y5 - coor_y1)
            length2 = hypot(coor_x17 - coor_x1, coor_y17 - coor_y1)
            horizontal_distance = abs(coor_x5 - coor_x1)
            vol = max(min(np.interp(length, [15, 220], [MinVol, MaxVol]), 0.0), -65.25)
            adjvolume.SetMasterVolumeLevel(vol, None)
            is_hand_fully_open = False
            if length > 50 and length2 > 50:
                is_hand_fully_open = True

            # Mimic hand movement with cursor movement
            if is_hand_fully_open:
                # Get the current position of the hand's index finger tip
                x_finger_tip = List_landmark[8][1]
                y_finger_tip = List_landmark[8][2]
                x_finger_tip = int(x_finger_tip * x_scale)
                y_finger_tip = int(y_finger_tip * y_scale)
                x_finger_tip = x_finger_tip
                # Move the cursor to the position of the index finger tip
                pyautogui.moveTo(screen_width - x_finger_tip, y_finger_tip)

            if length < 20:
                if not left_click:
                    left_click = True
                    pyautogui.click(button='left')
            else:
                if left_click:
                    left_click = False

            if length2 < 20:
                if not right_click:
                    right_click = True
                    pyautogui.click(button='right')
            else:
                if right_click:
                    right_click = False

            print("Volume:", vol, "Horizontal Distance:", horizontal_distance, "Left Click:", left_click, "Right Click:", right_click)


    cv2.imshow('Image', frame_img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

ccap.release()
cv2.destroyAllWindows()
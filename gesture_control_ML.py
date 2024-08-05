import cv2
import numpy as np
import sys
import pyautogui as pai
from detect_hand import hdet
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
import math

pai.FAILSAFE = False
scr_wid, scr_ht = pai.size()
print(scr_wid, scr_ht)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
cap = cv2.VideoCapture(0)

min_YCrCb = np.array([0, 130, 70], np.uint8)
max_YCrCb = np.array([255, 180, 130], np.uint8)

MAX_VOLUME = -0.01
MIN_VOLUME = -65.25

# Convert percentage to dB
def percentage_to_db(percent):
    if percent <= 0:
        return MIN_VOLUME
    elif percent >= 100:
        return MAX_VOLUME
    else:
        return (20 * math.log10(percent / 100)) - 20

def set_master_volume_percentage(percent):
    # Convert percentage to dB
    volume_level = percentage_to_db(percent)

    # Set the master volume level
    volume.SetMasterVolumeLevel(volume_level, None)

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    mx, my, cat = hdet(frame, min_YCrCb, max_YCrCb)
    print("Value of cat is : "+cat)
    if mx == 0 and my == 0:
        # sys.exit()
        print("exit was called here")

    if cat == '0':
        cv2.putText(frame, "Volume 0%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(0)
    elif cat == '1':
        cv2.putText(frame, "Volume 10%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(10)
    elif cat == '2':
        cv2.putText(frame, "Volume 20%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(20)
    elif cat == '3':
        cv2.putText(frame, "Volume 30%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(30)
    elif cat == '4':
        cv2.putText(frame, "Volume 40%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(40)
    elif cat == '5':
        cv2.putText(frame, "Volume 50%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(50)
    elif cat == '6':
        cv2.putText(frame, "Volume 60%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(60)
    elif cat == '7':
        cv2.putText(frame, "Volume 70%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(70)
    elif cat == '8':
        cv2.putText(frame, "Volume 80%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(80)
    elif cat == '9':
        cv2.putText(frame, "Volume 100%", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        set_master_volume_percentage(100)
    else:
        cv2.putText(frame, "Alphabet", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

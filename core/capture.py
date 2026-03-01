import mss
import numpy as np
import cv2

def capture_region(rect):
    with mss.mss() as sct:
        monitor = {
            "left": rect[0],
            "top": rect[1],
            "width": rect[2] - rect[0],
            "height": rect[3] - rect[1],
        }
        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
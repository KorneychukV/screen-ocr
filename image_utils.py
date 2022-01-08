from PIL import ImageGrab
import numpy as np
import cv2 as cv
import tkinter

def get_screenshot():
    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    img = ImageGrab.grab(bbox=(0, 0, width, height))
    img_np = np.array(img)
    # frame = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
    return img_np, width, height

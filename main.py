import cv2 as cv
import numpy as np

import image_utils as iu
import easyocr

x1, y1, x2, y2 = 0, 0, 0, 0

def draw_circle(event,x,y,flags,param):
    global x1, y1, x2, y2, stop_select
    if event == cv.EVENT_LBUTTONDOWN:
        x1, y1 = x,y
        print('down', x1, y1)

    if event == cv.EVENT_LBUTTONUP:
        stop_select = True
        x2, y2 = x,y
        if (x1 > x2) or (y1 > y2):
            x1, y1 = x2, y2
        print('up', x2, y2)

if __name__ == '__main__':
    stop_select = False
    img, width, height = iu.get_screenshot()
    cv.namedWindow('screenshot', cv.WINDOW_NORMAL)
    cv.resizeWindow('screenshot', width, height)
    cv.imshow("screenshot", img)
    cv.setMouseCallback('screenshot', draw_circle)
    is_continue = True

    while is_continue:
        if stop_select:
            img_copy = img.copy()
            cv.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0))
            cv.imshow("screenshot", img_copy)
            stop_select = False
        pushed_key = cv.waitKey(1)
        if pushed_key == 13:
            img = img[y1:y2, x1:x2]
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            img = np.invert(img)
            _, img = cv.threshold(img, 50, 255, cv.THRESH_BINARY_INV)
            img = cv.blur(img, (2, 2))
            pad = np.full((img.shape[0]+50, img.shape[1]+50), 255, dtype='uint8')
            pad[25:25+img.shape[0], 25:25+img.shape[1]] = img
            img = pad
            cv.imshow("screenshot", img)
            cv.resizeWindow('screenshot', img.shape[1]+50, img.shape[0]+50)
            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.recognize(img)
            for line in result:
                print(line[1])
        if pushed_key == 27:
            cv.destroyAllWindows()
            is_continue = False
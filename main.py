import cv2
import numpy as np

import os

import translator_gui
import OCR
import file_managment



cv2.namedWindow(OCR.OCR.window_name, cv2.WINDOW_AUTOSIZE)

language = OCR.chinese


def main():
    current_file = None
    try:

        while True:
            translator_gui.root.update()

            path, filename = file_managment.get_recent_images()
            if path:
                file_managment.move_file(path, '.')
                if current_file:
                    os.remove(current_file)
                current_file = filename


                translator_gui.translate(filename)



            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        # deletes all remaining images
        desktop = (os.listdir('./'))
        for name in desktop:
            if '.png' in name and name != 'noimage.png':
                os.remove(f'./{name}')

print('OCR Ready')
main()
cv2.destroyWindow(OCR.OCR.window_name)

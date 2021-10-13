import cv2
import numpy as np
import time
import pathlib
import os
import shutil
from datetime import datetime

from OCR import OCR


def check_recent_images(name):
    date = str(datetime.now()).split(' ')[0]

    if 'Screen Shot' in name:
        if '2021' in name:
            if date in name:

                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                h, m, s = map(int, str(current_time).split(':'))
                h2, m2, s2 = map(int, str(name).split(' ')[-2].split('.'))
                return abs(m - m2) < 2
    return False




home = str(pathlib.Path.home())
cv2.namedWindow(OCR.window_name, cv2.WINDOW_AUTOSIZE)
def main():
    while True:
        desktop = (os.listdir(home + '/Desktop'))
        for name in desktop:
            full_path = f'{home}/Desktop/{name}'

            if check_recent_images(name):
                shutil.move(full_path, '.')
                ocr = OCR('cht', name)  # 'cht' - chinese traditional, 'chs' - chinese simplified
                ocr.translate_image()
                ocr.print_text()
                ocr.print_pinyin()
                horizontal = np.concatenate(ocr.annotate_image(), axis=1)
                cv2.imshow(OCR.window_name, horizontal)

                os.remove(f'./{name}')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


print('OCR Ready')
main()
cv2.destroyWindow(OCR.window_name)

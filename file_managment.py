import os
import time
import shutil
import pathlib
from datetime import datetime
from PIL import Image as im

home = str(pathlib.Path.home())

def get_recent_images():
    desktop = (os.listdir(home + '/Desktop'))
    date = str(datetime.now()).split(' ')[0]
    for name in desktop:
        full_path = f'{home}/Desktop/{name}'
        if 'Screen Shot' in name:
            if '2022' in name:
                if date in name:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    h, m, s = map(int, str(current_time).split(':'))
                    h2, m2, s2 = map(int, str(name).split(' ')[-2].split('.'))
                    if abs(m - m2) < 2:
                        return full_path, name
    return None, None

def move_file(path, new_path):
    shutil.move(path, new_path)

def save_image(arr, path):
    data = im.fromarray(arr)
    data.save(path)



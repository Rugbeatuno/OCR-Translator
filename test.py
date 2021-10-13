import mss
import numpy as np
import time
import pyautogui
from PIL import Image
from pynput.mouse import Controller, Button

controller = Controller()

baseline = 0
monitor = {"top": 1, "left": 1, "width": 240, "height": 30}  # game dimensions
width, height = pyautogui.size()
midX, midY = width/2, height/2
monitor['top'] = midY - 40
monitor['left'] = midX - 120

x = [10, 85, 150, 225, 300, 370, 444]
y = 415

resting = (740, 480)

# mouse coords
pos = {
    1: (610, y),
    2: (650, y),
    3: (690, y),
    4: (720, y),
    5: (750, y),
    6: (790, y),
    7: (830, y),
}


# rgb values of the clay
clay = [
    [98, 76, 146],
    [27, 129, 159],
    [16, 121, 74],
    [16, 73, 55],
    [111, 27, 81],
    [95, 31, 31],
    [141, 117, 40],
]


def screenshot():
    while True:
        # time.sleep(0.03)
        # time.sleep(0.06)
        # time.sleep(0.13)
        with mss.mss() as sct:
            raw_pixels = sct.grab(monitor)
            screen = np.array(raw_pixels)
            # rgb = screen[35][x[0]][:-1]
            # print(rgb)

            for index, x_ in enumerate(x):
                rgb = screen[35][x_][:-1]
                rgb = list(rgb)

                # if rgb == clay[index]:
                if abs(sum(rgb)/3 - sum([140, 146, 152])/3) < 3:
                    index += 1
                    controller.position = pos[index]
                    pyautogui.middleClick()
                    # pyautogui.press('q')
                    time.sleep(0.025)
                    controller.position = resting

            #
            # img = Image.frombytes("RGB", raw_pixels.size, raw_pixels.bgra, "raw", "BGRX")
            # img.save(".." + "/OCR Translator/image.png")

def automine():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('w')
    pyautogui.mouseDown()
    # time.sleep(95)
    # pyautogui.keyUp('alt')
    # pyautogui.keyUp('w')
    # pyautogui.mouseUp()
    #
    # time.sleep(1)
    # pyautogui.write('/craft', 0.5)
    # pyautogui.press('enter')
    #
    #
    # pyautogui.moveTo(830, 318, 1)
    # pyautogui.click(clicks=15, interval=0.2)
    # time.sleep(1)
    # pyautogui.press('e')
    # time.sleep(2)
    # automine()


def aimassist():
    while True:
        pyautogui.keyDown('shift')
        print('ok')
        time.sleep(1)
        pyautogui.keyUp('shift')
        time.sleep(21)

import keyboard
def caneplant():
    time.sleep(3)
    pyautogui.keyDown('shift')
    time.sleep(1)
    pyautogui.keyDown('s')
    cycles = 0
    cps = 6

    while True:
        controller.click(Button.right)
        cycles += 1
        time.sleep(1/cps)
        if cycles == 64:
            pyautogui.scroll(-1)
            cycles = 0

        if keyboard.is_pressed('k'):
            pyautogui.keyUp('shift')
            pyautogui.keyUp('s')
            time.sleep(0.1)
            pyautogui.press('e')
            pyautogui.press('s')
            pyautogui.press('shift')
            pyautogui.press('e')
            quit()

def caneharvest():
    pyautogui.mouseDown()
    while True:
        pyautogui.keyDown('a')
        time.sleep(20)
        pyautogui.keyUp('a')
        pyautogui.keyDown('w')
        time.sleep(2)
        pyautogui.keyUp('w')
        pyautogui.keyDown('s')
        time.sleep(20)
        pyautogui.keyUp('s')
        pyautogui.keyDown('d')
        time.sleep(2)
        pyautogui.keyUp('d')


# os.system('sudo python3 test.py')
time.sleep(3)
automine()
# screenshot()
# caneplant()ee
# aimassist()
# caneharvest()
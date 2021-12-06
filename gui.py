import tkinter as tk
from tkinter import *


from OCR import OCR
import conversions


bg_color = '#121212'
# bg_color = '#222222'
bg_color2 = '#242525'

root = tk.Tk()
root.maxsize(height=1200, width=1600)
root.minsize(height=600, width=800)
root.configure(bg=bg_color)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


toolbar = tk.Frame(root, bg=bg_color)
toolbar.grid(row=0)

options = conversions.ocr_languages.keys()

label = Label(toolbar, text='Translate from: ', bg=bg_color, fg='white')
label.grid(row=0, column=0)

ocr = None
def translate(filepath='', changed=None):
    global ocr
    if filepath:
        change_image(filepath)
        root.update()
        ocr = OCR(filepath)

    if changed == 'input' or changed is None:
        print('ok')
        ocr.translate_image()
    ocr_text = ocr.translated_text
    translated_text = ocr.translate_text(ocr_text)
    set_english_translated(translated_text)
    set_ocr_translated(ocr_text)
    root.update()
    ocr.print_text()


def change_input_language(choice):
    choice = input_defualt.get()
    OCR.input_language = conversions.ocr_languages[choice]
    translate(changed='input')

def change_output_language(choice):
    choice = output_defualt.get()
    OCR.output_language = conversions.ocr_languages[choice]
    translate(changed='output')


input_defualt = StringVar()
input_defualt.set("English")
input_lang = OptionMenu(toolbar, input_defualt, *options, command=change_input_language)
input_lang.grid(row=0, column=1)

label = Label(toolbar, text=' to ', bg=bg_color, fg='white')
label.grid(row=0, column=2)

output_defualt = StringVar()
output_defualt.set("English")
output_lang = OptionMenu(toolbar, output_defualt, *options, command=change_output_language)
output_lang.grid(row=0, column=3)


image_area = tk.Frame(root, bg=bg_color)
image_area.grid(row=1)


canvas_height = 1000
unit_scalar = 13
padx = (10, 10)
pady = (5, 5)

img = PhotoImage(file="noimage.png")
canvas = Label(image_area, image=img, width=1000, height=canvas_height, bg=bg_color)
canvas.grid(rowspan=2)

english_translated = Text(image_area, height=canvas_height/2/unit_scalar, width=52, bg=bg_color2, fg='white', highlightthickness=0)
english_translated.grid(row=0, column=1, padx=padx, pady=pady)

ocr_translated = Text(image_area, height=canvas_height/2/unit_scalar, width=52, bg=bg_color2, fg='white', highlightthickness=0)
ocr_translated.grid(row=1, column=1, padx=padx, pady=pady)

def change_image(path):
    img = PhotoImage(file=path)
    canvas.configure(image=img)
    canvas.image = img

def set_english_translated(text):
    english_translated.delete(1.0, END)
    english_translated.insert(1.0, text)

def set_ocr_translated(text):
    ocr_translated.delete(1.0, END)
    ocr_translated.insert(1.0, text)

root.update()


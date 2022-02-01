import tkinter as tk
from tkinter.ttk import Style

from OCR import OCR
import conversions


bg_color = '#1E1D20'
bg_color2 = '#161617'
button_color = '#0A4E8A'

root = tk.Tk("Translator")
root.maxsize(height=1200, width=1600)
root.minsize(height=600, width=800)
root.config(bg=bg_color)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()



ocr = None
def translate(filepath='', changed=None):
    global ocr
    if filepath:  # when a new image is introduced
        change_image(filepath)
        root.update()
        ocr = OCR(filepath)

    # when the input language is changed or a new image is introduced
    if changed == 'input' or changed is None:
        ocr.translate_image()
        ocr.annotate_image()

    ocr_text = ocr.translated_text
    translated_text = ocr.translate_text(ocr_text)
    set_english_translated(translated_text)
    set_ocr_translated(ocr_text)
    ocr.print_text()

    root.update()


def change_input_language(_):
    choice = input_default.get()
    OCR.input_language = conversions.ocr_languages[choice]
    translate(changed='input')

def change_output_language(_):
    choice = output_default.get()
    OCR.output_language = conversions.ocr_languages[choice]
    translate(changed='output')

def cycle_image():
    global ocr
    change_image(ocr.get_next_image())

def resize_image(scale):
    global ocr
    ocr.image_scalar += scale
    ocr.scale_images()
    # cycle_image()


toolbar = tk.Frame(root, bg=bg_color)
toolbar.grid(row=0, column=0)



label = tk.Label(toolbar, text='Translate from: ', bg=bg_color, fg='white')
label.grid(row=0, column=0)

options = conversions.ocr_languages.keys()
input_default = tk.StringVar()
input_default.set("English")
input_lang = tk.OptionMenu(toolbar, input_default, *options, command=change_input_language)
input_lang.grid(row=0, column=1)
input_lang.config(bg=bg_color)

label = tk.Label(toolbar, text=' -> ', bg=bg_color, fg='white')
label.grid(row=0, column=2)

output_default = tk.StringVar()
output_default.set("English")
output_lang = tk.OptionMenu(toolbar, output_default, *options, command=change_output_language)
output_lang.grid(row=0, column=3)
output_lang.config(bg=bg_color)



switch_image = tk.Button(toolbar, text='Switch Image', bg=button_color, highlightbackground=bg_color, command=cycle_image)
switch_image.grid(row=0, column=4, padx=(50, 0))
switch_image = tk.Button(toolbar, text='+', bg=button_color, highlightbackground=bg_color, command=lambda: resize_image(0.1))
switch_image.grid(row=0, column=5, padx=5)
switch_image = tk.Button(toolbar, text='-', bg=button_color, highlightbackground=bg_color, command=lambda: resize_image(-0.1))
switch_image.grid(row=0, column=6)

image_area = tk.Frame(root, bg='#34383E')
image_area.grid(row=2)


canvas_height = 1000
unit_scalar = 13
padx = (10, 10)
pady = (5, 5)

img = tk.PhotoImage(file="noimage.png")
canvas = tk.Label(image_area, image=img, width=1000, height=canvas_height, bg='#262D31')
canvas.grid(rowspan=2)

english_translated = tk.Text(image_area, height=canvas_height/2/unit_scalar, width=52, bg=bg_color2, fg='white', highlightthickness=0)
english_translated.grid(row=0, column=1, padx=padx, pady=pady)

ocr_translated = tk.Text(image_area, height=canvas_height/2/unit_scalar, width=52, bg=bg_color2, fg='white', highlightthickness=0)
ocr_translated.grid(row=1, column=1, padx=padx, pady=pady)

def change_image(path):
    img = tk.PhotoImage(file=path)
    canvas.configure(image=img)
    canvas.image = img

def set_english_translated(text):
    english_translated.delete(1.0, tk.END)
    english_translated.insert(1.0, text)

def set_ocr_translated(text):
    ocr_translated.delete(1.0, tk.END)
    ocr_translated.insert(1.0, text)

root.update()


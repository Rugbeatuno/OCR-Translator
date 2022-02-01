# data imports
import requests
import json
import io
from itertools import cycle

# OCR imports
import cv2
from googletrans import Translator
import pinyin
import numpy as np
from matplotlib import pyplot as plt

from conversions import ocr_to_text, text_languages
from file_managment import save_image

chinese = 'cht'

class OCR:
    window_name = 'Translated'
    url = 'https://api.ocr.space/parse/image'
    key = '086f51a0ba88957'
    translator = Translator()
    font = cv2.FONT_HERSHEY_PLAIN

    input_language = 'eng'
    output_language = 'eng'

    def __init__(self, name):
        self.filename = name
        self.filepath = f'./{self.filename}'
        self.lines = []
        self.translated_text = ''
        self.images = []
        self.image_scalar = 1.0
        self.original_w_h = ()

    def annotate_image(self):
        img = cv2.imread(self.filepath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pinyin_mask = np.zeros_like(img)
        english_mask = np.zeros_like(img)

        # 図一白\r\n里\r\nRACK\r\nWINTER\r\nWHITE\r\n
        translated = self.translate_text(self.translated_text)
        line_text = translated.split('\r\n')
        buffer = 5

        for index, line in enumerate(self.lines):

            for word in line['Words']:
                text = word['WordText']
                x = int(word['Left'])
                y = int(word['Top'])
                height = int(word['Height'])
                width = int(word['Width'])

                font_scale = width / 40
                # cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 255), -1)
                cv2.putText(pinyin_mask, self.get_pinyin(text), (int(x + buffer), int(y + buffer)), OCR.font, font_scale, (255, 255, 255), int(font_scale))

            x = int(line['Words'][0]['Left'])
            y = int(line['Words'][0]['Top'])
            height = int(line['Words'][0]['Height'])
            width = int(line['Words'][0]['Width'])
            font_scale = width / 30
            font_scale = font_scale if font_scale > 1 else 1

            cv2.putText(english_mask, line_text[index], (int(x), int(y + height / 2)), OCR.font, font_scale, (255, 255, 255), 1)

        # if language == chinese:
        #     ocr.print_pinyin()
        #     pinyin_mask, english_mask, original = ocr.annotate_image()
        pinyin_mask = cv2.addWeighted(img, 0.2, pinyin_mask, 1, 0)
        english_mask = cv2.addWeighted(img, 0.2, english_mask, 1, 0)
        #     horizontal = np.concatenate(np.array([pinyin, english]), axis=0)
        #     cv2.imshow(OCR.window_name, horizontal)r

        original = './original.png'
        english = './english.png'
        pinyin = './pinyin.png'
        save_image(img, original)
        save_image(english_mask, english)
        save_image(pinyin_mask, pinyin)
        self.images = [original, english, pinyin]
        self.cycle = cycle(self.images)
        next(self.cycle)  # starts off with the first image


    # compresses image and sends to OCR API and gets results
    def translate_image(self):
        file = cv2.imread(self.filepath)
        h, w, c = file.shape
        self.original_w_h = (w, h)
        self.image_scalar = 1.0

        _, compressed_image = cv2.imencode(".png", file, [1, 90])
        file_bytes = io.BytesIO(compressed_image)

        result = requests.post(OCR.url, files={self.filepath: file_bytes},
                               data={
                                   'apikey': OCR.key,
                                   'language': OCR.input_language,
                                   'scale': True,
                                   'isOverlayRequired': True
                               })

        decoded_result = result.content.decode()
        data = json.loads(decoded_result)
        data = data['ParsedResults'][0]


        try:
            self.lines = [i for i in data['TextOverlay']['Lines']]
            self.translated_text = str(data['ParsedText'])
        except KeyError:
            self.translated_text = "None Found."


    def translate_text(self, text):
        return str(OCR.translator.translate(text, src=text_languages[ocr_to_text[OCR.input_language]], dest=text_languages[ocr_to_text[OCR.output_language]]).text)

    def get_pinyin(self, text):
        return str(pinyin.get(text, format="strip"))  # change format to numerical for numbered pinyin

    def print_pinyin(self):
        for char in self.translated_text:
            if len(char) == 1:
                print(f'{char}  {pinyin.get(str(char))}')

    def print_text(self):
        if self.input_language == chinese:
            print(f'{self.translated_text} --> {self.translate_text(self.translated_text)}')
        else:
            print(self.translated_text)

    def get_next_image(self):
        return next(self.cycle)

    def scale_images(self):
        original = './original.png'
        english = './english.png'
        pinyin = './pinyin.png'

        original_image = cv2.imread(original)
        english_image = cv2.imread(original)
        pinyin_image = cv2.imread(original)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        english_image = cv2.cvtColor(english_image, cv2.COLOR_BGR2RGB)
        pinyin_image = cv2.cvtColor(pinyin_image, cv2.COLOR_BGR2RGB)
        new_size = (int(self.original_w_h[0] * self.image_scalar), int(self.original_w_h[1] * self.image_scalar))
        original_image = cv2.resize(original_image, new_size)
        english_image = cv2.resize(english_image, new_size)
        pinyin_image = cv2.resize(pinyin_image, new_size)

        save_image(original_image, original)
        save_image(english_image, english)
        save_image(pinyin_image, pinyin)


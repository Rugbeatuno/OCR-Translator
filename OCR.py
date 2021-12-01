# data imports
import requests
import json
import io

# OCR imports
import cv2
from googletrans import Translator
import pinyin
import numpy as np

chinese = 'cht'

class OCR:
    window_name = 'Translated'
    url = 'https://api.ocr.space/parse/image'
    key = '086f51a0ba88957'
    translator = Translator()
    font = cv2.FONT_HERSHEY_PLAIN

    def __init__(self, lang, name):
        self.language = lang
        self.filename = name
        self.filepath = f'./{self.filename}'
        self.lines = []
        self.translated_text = ''

    def annotate_image(self):
        img = cv2.imread(self.filepath)
        pinyin_mask = np.zeros_like(img)
        english_mask = np.zeros_like(img)


        for line in self.lines:
            for word in line['Words']:
                text = word['WordText']
                x = int(word['Left'])
                y = int(word['Top'])
                height = int(word['Height'])
                width = int(word['Width'])

                font_scale = width / 40
                # cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 255), -1)
                cv2.putText(pinyin_mask, self.get_pinyin(text), (int(x + width / 3), int(y + height / 2)), OCR.font, font_scale, (255, 255, 255), int(font_scale))

            line_text = line['LineText']
            x = int(line['Words'][0]['Left'])
            y = int(line['Words'][0]['Top'])
            height = int(line['Words'][0]['Height'])
            width = int(line['Words'][0]['Width'])
            font_scale = width / 25

            translated = self.translate_text(line_text)
            cv2.putText(english_mask, translated, (int(x), int(y + height / 2)), OCR.font, font_scale, (255, 255, 255), 1)
        return pinyin_mask, english_mask, img

    # compresses image and sends to OCR API and gets results
    def translate_image(self):
        file = cv2.imread(self.filepath)
        _, compressed_image = cv2.imencode(".png", file, [1, 90])
        file_bytes = io.BytesIO(compressed_image)

        result = requests.post(OCR.url, files={self.filepath: file_bytes},
                               data={
                                   'apikey': OCR.key,
                                   'language': self.language,
                                   'scale': True,
                                   'isOverlayRequired': True
                               })

        decoded_result = result.content.decode()
        data = json.loads(decoded_result)

        try:
            self.lines = [i for i in data['ParsedResults'][0]['TextOverlay']['Lines']]
            self.translated_text = str(data["ParsedResults"][0]['ParsedText'])
        except KeyError:
            self.translated_text = "None Found."

    def translate_text(self, text):
        return str(OCR.translator.translate(text, src='zh-tw', dest='en').text)

    def get_pinyin(self, text):
        return str(pinyin.get(text, format="strip"))  # change format to numerical for numbered pinyin

    def print_pinyin(self):
        for char in self.translated_text:
            if len(char) == 1:
                print(f'{char}  {pinyin.get(str(char))}')

    def print_text(self):
        if self.language == chinese:
            print(f'{self.translated_text} --> {self.translate_text(self.translated_text)}')
        else:
            print(self.translated_text)


from googletrans import Translator
translator = Translator()


print(str(translator.translate('hello', src='en', dest='jp').text))


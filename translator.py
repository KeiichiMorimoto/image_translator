from googletrans import Translator

def translate_en_to_ja(text):
    translator = Translator()
    return translated = translator.translate(txt, dest="ja")
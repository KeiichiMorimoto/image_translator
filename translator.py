from googletrans import Translator

def translate_en_to_ja(text):
    translator = Translator()
    translated = translator.translate(text, dest="ja")
    return translated.text
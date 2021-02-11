from PIL import Image
import sys
sys.path.append('/path/to/dir')

import pyocr
import pyocr.builders
from googletrans import Translator

def translate_eng_image_to_ja(image=None):
    print("translate_eng_image_to_ja : in")

    if image is None:
        return '必要な情報が足りません'

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    #print("Will use tool '%s'" % (tool.get_name()))

    langs = tool.get_available_languages()
    #print("Available languages: %s" % ", ".join(langs))

    txt = tool.image_to_string(
        Image.open(image),
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )
 
    translator = Translator()
    translated = translator.translate(txt, dest="ja")
    return translated.text

import pyocr
import pyocr.builders
import sys
from PIL import Image

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))

def readimg(path: str) -> str:
    """使用 pyocr 读取图片"""
    txt = tool.image_to_string(
        Image.open(path),
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    return txt.replace('\n', '').replace(' ', '').lower()
from PIL import Image
from Utils.AlphaConverter import convert_image


def resizeImage(path, size):
    img = Image.open(path)
    if img.mode[-1] == 'A':
        img = img.convert('RGBA')
        img = convert_image(img)
    img = img.resize(size)
    img.save(path)
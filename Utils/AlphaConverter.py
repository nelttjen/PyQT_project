from PIL import Image


def convert_image(img):
    img.load()
    back = Image.new("RGB", img.size, (255, 255, 255))
    back.paste(img, mask=img.split()[3])
    back.save('Images/Temp/convert.jpg', 'JPEG', quality=80)
    return Image.open('Images/Temp/convert.jpg')
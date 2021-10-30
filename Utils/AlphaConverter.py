from PIL import Image
import numpy as np


# def convert_image(front, back=Image.new(mode='RGBA', size=(1920, 1080), color=(255, 255, 255, 255))):
#     back = back.resize(front.size)
#     front = np.asarray(front)
#     back = np.asarray(back)
#     result = np.empty(front.shape, dtype='float')
#     alpha = np.index_exp[:, :, 3:]
#     rgb = np.index_exp[:, :, :3]
#     falpha = front[alpha] / 255.0
#     balpha = back[alpha] / 255.0
#     result[alpha] = falpha + balpha * (1 - falpha)
#     old_setting = np.seterr(invalid='ignore')
#     result[rgb] = (front[rgb] * falpha + back[rgb] * balpha * (1 - falpha)) / result[alpha]
#     np.seterr(**old_setting)
#     result[alpha] *= 255
#     np.clip(result, 0, 255)
#     result = result.astype('uint8')
#     result = Image.fromarray(result, 'RGBA')
#     return result

def convert_image(img):
    img.load()
    bckgr = Image.new("RGB", img.size, (255, 255, 255))
    bckgr.paste(img, mask=img.split()[3])
    bckgr.save('Images/Temp/convert.jpg', 'JPEG', quality=80)
    return Image.open('Images/Temp/convert.jpg')
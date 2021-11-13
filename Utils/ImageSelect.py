from PIL import Image
from Utils.Values import GRID_PATTERN_SIZE


def image_select(pattern_name):
    try:
        p_img = Image.open(f'./Images/Patterns/Preview/{pattern_name}.png')
    except FileNotFoundError:
        p_img = Image.new('RGB', GRID_PATTERN_SIZE, color='black')
    background = Image.new(mode='RGB', size=(p_img.size[0] + 10, p_img.size[1] + 10), color='yellow')
    background.paste(p_img, (5, 5))
    selected = background.resize(p_img.size)
    selected.save('./Images/Temp/select.png')


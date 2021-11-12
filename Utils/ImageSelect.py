from PIL import Image


def image_select(pattern_name):
    try:
        p_img = Image.open(f'./Images/Patterns/Preview/{pattern_name}.png')
        background = Image.new(mode='RGB', size=(p_img.size[0] + 10, p_img.size[1] + 10), color='yellow')
        background.paste(p_img, (5, 5))
        selected = background.resize(p_img.size)
        selected.save('./Images/Temp/select.png')
    except Exception as e:
        print(e)

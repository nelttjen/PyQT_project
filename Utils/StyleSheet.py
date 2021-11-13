def add_style_sheet(buttons):
    for i in buttons:
        i.setStyleSheet(open('./Data/style.css').read())

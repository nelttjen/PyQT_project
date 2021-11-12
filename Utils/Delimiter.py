def text_delimiter(text, delimiter):
    text = text.split()
    temp_text = []
    tmp_count = 0
    for i in range(len(text)):
        if tmp_count == delimiter:
            tmp_count = 0
            temp_text[i - 1] = f'{temp_text[i - 1]}\n'
        temp_text.append(text[i])
        tmp_count += 1
    text = ' '.join(temp_text)
    return text.replace('\n ', '\n')

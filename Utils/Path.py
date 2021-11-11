def get_name_from_path(path):
    return path.replace('./', '').replace('Images/Patterns/', '')\
        .replace('Custom/', '').replace('Preview/', '').replace('.png', '')


def get_path_to_pattern(pattern_id):
    pattern_id = get_name_from_path(pattern_id)
    return f'./Images/Patterns/{pattern_id}.png'


def get_path_to_preview(pattern_id):
    pattern_id = get_name_from_path(pattern_id)
    return f'./Images/Patterns/Preview/{pattern_id}.png'


def get_clean_id(path):
    pattern = get_name_from_path(path)
    return pattern.replace('pattern', '')

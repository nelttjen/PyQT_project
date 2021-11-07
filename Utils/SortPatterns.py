from Utils.Path import get_clean_id


def sort_patterns(patterns):
    return sorted(patterns, key=lambda x: int(get_clean_id(x.replace('pattern', '').replace('.png', ''))))

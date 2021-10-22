def sortPatterns(patterns):
    return sorted(patterns, key=lambda x: int(x.replace('pattern', '').replace('.png', '')))
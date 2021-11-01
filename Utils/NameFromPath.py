def getNameFromPath(path):
    return path.replace('./', '').replace('Images/Patterns/', '').replace('Preview/', '').replace('.png', '')
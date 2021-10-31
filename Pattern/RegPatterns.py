import json
import os

from Pattern.Pattern import Pattern
from Utils.SortPatterns import sortPatterns

patterns = []


def registerPatterns():
    pathToPatterns = './Images/Patterns'
    filenames = os.listdir(pathToPatterns)[:-1]
    filenames = sortPatterns(filenames)
    keys = ['line1', 'line2',
            'image1', 'image2',
            'text1Size', 'text2Size',
            'text1Delimiter', 'text2Delimiter',
            'line1XY', 'line2XY',
            'image1XY', 'image2XY',
            'line1Size', 'line2Size',
            'image1Size', 'image2Size',
            'text1Align', 'text2Align']
    with open('Json/PatternProperties.json', 'r') as jsonFile:
        json_data = json.load(jsonFile)
    for i in filenames:
        if i.replace('.png', '') in list(json_data.keys()):
            existKeys = []
            temp_data = {}
            for k in keys:
                if k in list(json_data[i.replace('.png', '')].keys()):
                    existKeys.append(k)
            for k in keys:
                if k in existKeys:
                    if k == 'line1' or k == 'line2' or k == 'image1' or k == 'image2':
                        temp_data[k] = True if json_data[i.replace('.png', '')][k] == 1 else False
                    else:
                        temp_data[k] = json_data[i.replace('.png', '')][k]
                else:
                    if k == 'line1' or k == 'line2' or k == 'image1' or k == 'image2':
                        temp_data[k] = False
                    elif k == 'text1Size' or k == 'text2Size' or k == 'text1Delimiter' or k == 'text2Delimiter':
                        temp_data[k] = 0
                    elif k == 'line1XY' or k == 'line2XY' or k == 'image1XY' or k == 'image2XY' \
                            or k == 'image1Size' or k == 'image2Size' or k == 'line1Size' or k == 'line2Size':
                        temp_data[k] = (0, 0)
                    elif k == 'text1Align' or k == 'text2Align':
                        temp_data[k] = 'center'

            new_pattern = Pattern(line1=temp_data[keys[0]], line2=temp_data[keys[1]],
                                  image1=temp_data[keys[2]], image2=temp_data[keys[3]],
                                  text1Size=temp_data[keys[4]], text2Size=temp_data[keys[5]],
                                  text1Delimiter=temp_data[keys[6]], text2Delimiter=temp_data[keys[7]],
                                  line1XY=tuple(temp_data[keys[8]]), line2XY=tuple(temp_data[keys[9]]),
                                  image1XY=tuple(temp_data[keys[10]]), image2XY=tuple(temp_data[keys[11]]),
                                  line1Size=tuple(temp_data[keys[12]]), line2Size=tuple(temp_data[keys[13]]),
                                  image1Size=tuple(temp_data[keys[14]]), image2Size=tuple(temp_data[keys[15]]),
                                  text1Align=temp_data[keys[16]], text2Align=temp_data[keys[17]],
                                  filePath=f'{pathToPatterns}/{i}')
            patterns.append(new_pattern)
    return patterns

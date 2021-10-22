import json
import os

from Utils.SortPatterns import sortPatterns

patterns = []


class Pattern:
    def __init__(self, line1=False, line2=False,
                 image1=False, image2=False,
                 text1Size=0, text2Size=0,
                 line1XY=(0, 0), line2XY=(0, 0),
                 image1XY=(0, 0), image2XY=(0, 0),
                 line1Size=(0, 0), line2Size=(0, 0),
                 image1Size=(0, 0), image2Size=(0, 0),
                 filePath=None):

        self.filePath = filePath

        self.line1 = line1
        self.line2 = line2
        self.line1XY = line1XY if self.line1 else None
        self.line2XY = line2XY if self.line2 else None
        self.line1Size = line1Size if self.line1 else None
        self.line2Size = line2Size if self.line2 else None
        self.text1Size = text1Size if self.line1 else None
        self.text2Size = text2Size if self.line2 else None

        self.image1_exist = image1
        self.image2_exist = image2
        self.image1XY = image1XY if self.image1_exist else None
        self.image2XY = image2XY if self.image2_exist else None
        self.image1SSize = image1Size if self.image1_exist else None
        self.image2SSize = image2Size if self.image2_exist else None

    def getObject(self):
        return [self.filePath,
                [self.line1, self.line1XY, self.line1Size, self.text1Size],
                [self.line2, self.line2XY, self.line2Size, self.text2Size],
                [self.image1_exist, self.image1XY, self.image1SSize],
                [self.image2_exist, self.image2XY, self.image2SSize]]


def registerPatterns():
    pathToPatterns = './Images/Patterns'
    filenames = os.listdir(pathToPatterns)[:-1]
    filenames = sortPatterns(filenames)
    keys = ['line1', 'line2',
            'image1', 'image2',
            'text1Size', 'text2Size',
            'line1XY', 'line2XY',
            'image1XY', 'image2XY',
            'line1Size', 'line2Size',
            'image1Size', 'image2Size']
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
                    elif k == 'text1Size' or k == 'text2Size':
                        temp_data[k] = 0
                    elif k == 'line1XY' or k == 'line2XY' or k == 'image1XY' or k == 'image2XY' \
                            or k == 'image1Size' or k == 'image2Size' or k == 'line1Size' or k == 'line2Size':
                        temp_data[k] = (0, 0)

            new_pattern = Pattern(line1=temp_data[keys[0]], line2=temp_data[keys[1]],
                                  image1=temp_data[keys[2]], image2=temp_data[keys[3]],
                                  text1Size=temp_data[keys[4]], text2Size=temp_data[keys[5]],
                                  line1XY=tuple(temp_data[keys[6]]), line2XY=tuple(temp_data[keys[7]]),
                                  image1XY=tuple(temp_data[keys[8]]), image2XY=tuple(temp_data[keys[9]]),
                                  line1Size=tuple(temp_data[keys[10]]), line2Size=tuple(temp_data[keys[11]]),
                                  image1Size=tuple(temp_data[keys[12]]), image2Size=tuple(temp_data[keys[13]]),
                                  filePath=f'{pathToPatterns}/{i}')
            patterns.append(new_pattern)
    return patterns

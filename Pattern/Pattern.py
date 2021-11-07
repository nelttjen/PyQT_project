from Utils.Path import get_name_from_path


class Pattern:
    def __init__(self, line1=False, line2=False,
                 image1=False, image2=False,
                 text1Size=0, text2Size=0,
                 text1Delimiter=0, text2Delimiter=0,
                 text1Align='center', text2Align='center',
                 line1XY=(0, 0), line2XY=(0, 0),
                 image1XY=(0, 0), image2XY=(0, 0),
                 line1Size=(0, 0), line2Size=(0, 0),
                 image1Size=(0, 0), image2Size=(0, 0),
                 filePath=None, default=True):

        self.filePath = filePath
        self.isDefault = default

        self.line1 = line1
        self.line2 = line2
        self.line1XY = line1XY if self.line1 else None
        self.line2XY = line2XY if self.line2 else None
        self.line1Size = line1Size if self.line1 else None
        self.line2Size = line2Size if self.line2 else None
        self.text1Size = text1Size if self.line1 else None
        self.text2Size = text2Size if self.line2 else None
        self.text1Delimiter = text1Delimiter if self.line1 else None
        self.text2Delimiter = text2Delimiter if self.line2 else None
        self.text1Align = text1Align if self.line1 else None
        self.text2Align = text2Align if self.line2 else None

        self.image1_exist = image1
        self.image2_exist = image2
        self.image1XY = image1XY if self.image1_exist else None
        self.image2XY = image2XY if self.image2_exist else None
        self.image1SSize = image1Size if self.image1_exist else None
        self.image2SSize = image2Size if self.image2_exist else None

    def get_object(self):
        return [self.filePath,
                [self.line1, self.line1XY, self.line1Size, self.text1Size, self.text1Delimiter, self.text1Align],
                [self.line2, self.line2XY, self.line2Size, self.text2Size, self.text2Delimiter, self.text2Align],
                [self.image1_exist, self.image1XY, self.image1SSize],
                [self.image2_exist, self.image2XY, self.image2SSize],
                self.isDefault]


def find_pattern_by_id(patterns, pattern_id):
    for i in patterns:
        if get_name_from_path(i.get_object()[0]) == pattern_id:
            # Если найдет
            return i.get_object()
        else:
            continue
    return

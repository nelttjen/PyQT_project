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



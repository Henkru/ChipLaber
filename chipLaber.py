from PIL import Image, ImageDraw, ImageFont
from enum import Enum
import json

class PType(Enum):
    DIP8 = (25.4, 76)
    DIP32 = (25.4, 152)
    SOIC = (12.7, 60)

    @classmethod
    def getType(cls, name):
        if name == "DIP8":
            return PType.DIP8
        elif name == "DIP32":
            return PType.DIP32
        elif name == "SOIC":
            return PType.SOIC
        else:
            raise Exception("Unkown package type: %s" % name)

class Chip:
    def __init__(self, pins=[], name="", pType=PType.DIP8, fontSize=15):
        self.pins = pins
        self.name = name
        self.pType = pType

        self.icWidth = self.pType.value[1]
        self.pitch = self.pType.value[0]
        self.space = 10
        self.widthSpace = 4
        self.showName = True

        self.fontPath = "Fonts/courier.ttf"
        self.fontSize = fontSize
        self.nameFontSize = 15

    def generateImage(self):
        if len(self.pins) % 2:
            raise Exception("Pins count must be modulo by 2!")

        self.pinsPerSide = len(self.pins)/2

        self.height = int((self.pitch)*(self.pinsPerSide-0.5) + 2*self.space)
        self.width = self.icWidth

        self.im = Image.new("RGB", (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.im)
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)

        self.drawOuter()
        for i in range(0, len(self.pins)):
            self.drawLabel(i)

        if self.showName:
            self.drawName()

    def drawOuter(self):
        self.draw.rectangle([(0, 0), (self.width - 1, self.height - 1)], outline=0)

    def drawLabel(self, n):
        text = self.pins[n]

        upperLine = False
        if text[0] == "/":
            text = text[1:]
            upperLine = True
        textSize = self.draw.textsize(text, font=self.font)

        left = n < self.pinsPerSide
        x = self.widthSpace if left else self.width - textSize[0] - self.widthSpace/2

        y = self.pitch * n if left else self.pitch * (len(self.pins) - n - 1)
        y += self.space

        self.draw.text((x, y), text, font=self.font, fill=0)
        if upperLine:
            self.draw.line((x, y-2, x + textSize[0]-2, y-2), fill=0)

    def drawName(self):
        self.im = self.im.rotate(90, expand=1)
        self.draw = ImageDraw.Draw(self.im)

        nameFont = ImageFont.truetype(self.fontPath, self.nameFontSize)
        textSize = self.draw.textsize(self.name, font=nameFont)

        x = int(self.height/2 - textSize[0]/2)
        y = int(self.width/2 - textSize[1]/2)

        self.draw.text((x, y), self.name, font=nameFont, fill=0)

        self.im = self.im.rotate(-90, expand=1)
        self.draw = ImageDraw.Draw(self.im)

    def save(self, name):
        self.im.save(name, 'PNG')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("chip", help="Chip file", type=str)
    parser.add_argument("-s", "--size", type=int, help="Font size", default=15)
    parser.add_argument("-o", "--output", type=str, help="Output file", default=None)
    parser.add_argument("-hide", "--hide", action="store_true", help="Hide chip name")

    args = parser.parse_args()

    try:
        f = open(args.chip)
        data = json.load(f)

        pType = PType.getType(data['type'])
        img = Chip(data['pins'], data['name'], pType, args.size)
        img.showName = not args.hide
        img.generateImage()

        filename = args.output if args.output else "out/%s.png" % data['name']
        img.save(filename)
    except ValueError as ex:
        print("JSON file is not valid")
        print(ex)
    except KeyError as ex:
        print("'%s' missing in chip file." % ex.args[0])
    except Exception as ex:
        print(ex)

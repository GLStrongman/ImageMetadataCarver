# JPEG      Header: FF D8 FF E0 / ÿØÿà          Footer: FF D9 / ÿÙ
# PNG       Header: 89 50 4E 47 0D 0A 1A 0A     Footer: 49 45 4E 44 AE 42 60 82
# exiftool

from exif import Image
import re
import sys

headerJPEG = b'\xFF\xD8\xFF\xE0'
footerJPEG = b'\xFF\xD9'
headerPNG = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
footerPNG = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'

# Check that user has included a file 
if len(sys.argv) < 2:
    print("Please include a file name in the arguments")
    exit()

filepath = sys.argv[1]
file = open(filepath, 'rb')
contents = file.read()
file.close()

startPosJPEG = []
endPosJPEG = []
startPosPNG = []
endPosPNG = []

for match in re.finditer(re.escape(headerJPEG),contents):
    startPosJPEG.append(match.start())

for match in re.finditer(re.escape(footerJPEG),contents):
    endPosJPEG.append(match.start())

for match in re.finditer(re.escape(headerPNG),contents):
    startPosPNG.append(match.start())

for match in re.finditer(re.escape(footerPNG),contents):
    endPosPNG.append(match.start())

for i, pos in enumerate(startPosJPEG):
    print(f"JPEG {i} found, writing to JPEG_Image_{i}.jpg")
    pic = contents[pos:endPosJPEG[i]+2]
    filename = "JPEG_Image_" + str(i) + ".jpg"
    picFile = open(filename, 'wb')
    picFile.write(pic)

for i, pos in enumerate(startPosPNG):
    print(f"PNG {i} found, writing to PNG_Image_{i}.png")
    pic = contents[pos:endPosPNG[i]+9]
    filename = "PNG_Image_" + str(i) + ".png"
    picFile = open(filename, 'wb')
    picFile.write(pic)

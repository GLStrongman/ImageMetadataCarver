from exif import Image
import re
import sys

headerJPEG = b'\xFF\xD8\xFF\xE0'
footerJPEG = b'\xFF\xD9'
headerPNG = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
footerPNG = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
startPosJPEG = []
endPosJPEG = []
startPosPNG = []
endPosPNG = []

# Check that user has included a file 
if len(sys.argv) < 2:
    print("Please include a file name in the arguments")
    exit()

# Get contents of given file
try:
    filepath = sys.argv[1]
    file = open(filepath, 'rb')
    contents = file.read()
    file.close()
except:
    print("Error - couldn't open file, program exiting")
    exit()

# Look for headers and footers within the given file
for match in re.finditer(re.escape(headerJPEG),contents):
    startPosJPEG.append(match.start())

for match in re.finditer(re.escape(footerJPEG),contents):
    endPosJPEG.append(match.start())

for match in re.finditer(re.escape(headerPNG),contents):
    startPosPNG.append(match.start())

for match in re.finditer(re.escape(footerPNG),contents):
    endPosPNG.append(match.start())

# Extract images and write to files
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
    picFile.close()

# Find and print metadata
for i, pic in enumerate(startPosJPEG):
    filename = str("JPEG_Image_" + str(i) + ".jpg")
    image = Image(open(filename, 'rb'))
    if image.has_exif:
        print(f"{filename} metadata:")
        print("------------")
        print(f"Lens make: {image.get('lens_make', 'Unknown')}")
        print(f"Lens model: {image.get('lens_model', 'Unknown')}")
        print(f"Lens specification: {image.get('lens_specification', 'Unknown')}")
        print(f"OS version: {image.get('software', 'Unknown')}")
        print(f"Image timestamp: {image.datetime_original}")
        print(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
        print(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}")
    else:
        print(f"Image {filename} does not contain any metadata")

for i, pic in enumerate(startPosPNG):
    filename = str("PNG_Image_" + str(i) + ".png")
    image = Image(open(filename, 'rb'))
    if image.has_exif:
        print(f"{filename} metadata:")
        print("------------")
        print(f"Lens make: {image.get('lens_make', 'Unknown')}")
        print(f"Lens model: {image.get('lens_model', 'Unknown')}")
        print(f"Lens specification: {image.get('lens_specification', 'Unknown')}")
        print(f"OS version: {image.get('software', 'Unknown')}")
        print(f"Image timestamp: {image.datetime_original}")
        print(f"Latitude: {image.gps_latitude} {image.gps_latitude_ref}")
        print(f"Longitude: {image.gps_longitude} {image.gps_longitude_ref}")
    else:
        print(f"Image {filename} does not contain any metadata")

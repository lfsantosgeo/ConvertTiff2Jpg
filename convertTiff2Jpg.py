# -*- coding: utf-8 -*-
"""
@author Luiz Fernando dos Santos
        lfsantos(dot)geo(at)usp(dot)br

--------------------------------WHAT IT DOES?----------------------------------
Converts image format TIFF to JPEG using Image from PIL(LOW)
Afterwards gets the EXIF data from TIFF and appends to the JPEGs using Exiftool

It was made for a rapid conversion from TIFF files to JPG after the TIFF were
generated by DCRaw (converts RAW images into TIFF format)

------------------------------------USAGE--------------------------------------

1. Put the tiff files (might be 16bit or 8bit) on the script's directory
2. Run using command prompt "python converttiff2jpg.py" or run on interpreter

"""

import os                        # import OS module

# PILLOW is a fork of PIL Python Imaging Library. Adds image processing
# capabilities to the Python interpreter
# Image module provides image functios such as loading images from files and
# creating new images
from PIL import Image

# Subprocess is used to input ExifTool command into the prompt through Python
import subprocess


# defining a progress bar
def progressbar(count, total, status=""):
    bar_len = 40
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = "X" * filled_len + "-" * (bar_len - filled_len)

    print("\r[{}] {}{} ...{}".format(bar, percents, "%", status),
          end="", flush=True)


print("############### CONVERT TIFF TO JPG ##############")
print("-" * 50)
# get current working directory (script directory)

current_directory = os.getcwd()
print("CURRENT DIRECTORY: \n", current_directory)
# name the output directory
out_dir = os.path.join(current_directory, r"JPG")
print("OUTPUT DIRECTORY : \n", out_dir)
print("-" * 50 + "\n")

# create the output directory if non existent
if not os.path.exists(out_dir):
    try:
        os.makedirs(out_dir)
    except OSError as exc:
        print(exc)
        raise

# get the path to the output directory
output = os.chdir(os.path.dirname(os.getcwd()))

# generating filenames in a directory tree with os.walk()
for root, dirs, files in os.walk(current_directory, topdown=False):
    for name in files:
        # If there are TIFF files on current directory
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
            # Check if there are JPEGs in output directory
            if os.path.isfile(os.path.splitext(os.path.join(out_dir,
                                                            name))[0] +
                              ".jpg"):
                print("A JPEG file already exists for {}".format(name))

            # Then if JPEGs are absent, create JPEGs from the TIFFs
            else:
                # Get the files (images) names
                filename = os.path.splitext(os.path.join(name))[0]
                # Gets it lower case and adds the extension format JPEG
                outfile = filename.lower() + ".jpg"
                # Opens every image from script (current) directory with Image
                im = Image.open(os.path.join(root, name))
                print("Opening TIFF {}".format(name))

                # saving with a different format
                # quality above 95 disable portions of the JPEG compression
                # algorithm resulting in large files with no gain in image
                # quality
                im.save(out_dir + "//" + outfile, "jpeg", quality=100)
                print("Saving  JPEG {} \n".format(name))

print("\n")
print("-" * 50 + "\n")
# listing TIFF images
imagesT = [fn for fn in os.listdir(current_directory) if fn.endswith(".tiff")]
print("TIFF Image list: ", imagesT)
lenght = len(imagesT)
print("\nA total of {} TIFF images were listed...\n".format(lenght))

# listing JPEG images
imagesJ = [fn for fn in os.listdir(out_dir) if fn.endswith(".jpg")]
print("JPEG Image list: ", imagesJ)
lenght = len(imagesJ)
print("\nA total of {} TIFF images were saved into JPEG".format(lenght))

print("\n")
print("-" * 50 + "\n")
print("Please wait! Copying EXIF data from TIFFs to the new JPG files...\n")

# setting path and filename of TIFF images
for image in imagesT:
    c_path = os.path.join(current_directory, image)

# progress bar settings
i = 0
total = int(lenght)
# setting path and filename of JPEG images
for image in imagesJ:
    n_path = os.path.join(out_dir, image)

    # calling progress bar
    i += 1
    progressbar(i, total, status="EXIF copying...")

    # python to command line to use ExifTool
    cmd = 'exiftool -overwrite_original -TagsFromFile {0} -all:all {1}'.format(os.path.abspath(c_path), os.path.abspath(n_path)).split(' ')

    try:
        subprocess.call(cmd)
    except Exception as err:
        print("\nFailed to write to exif: {}".format(err))

print("\n\nScript done!")

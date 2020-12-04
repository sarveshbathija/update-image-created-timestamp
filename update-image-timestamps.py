import os
from datetime import datetime
import piexif

rootdir = '/Users/myHomeDirectory/allMyPictures'

for  subdir, dirs, files in os.walk(rootdir):
    directory = os.path.relpath(subdir)

    print('Found directory: %s' % directory)

    directory_pieces = directory.split(' ')
    date_pieces = directory_pieces[0].split('_');

    extension = ['jpg', 'JPG', 'jpeg', 'JPEG'];

    try:
        date_pieces[1]
    except IndexError:
        date_pieces.append(1)

    try:
    	date_pieces[2]
    except IndexError:
    	date_pieces.append(1)


    for filename in files:
        if any (x in filename for x in extension):
            print('----Editing timestamp for file: %s' % filename)
            print(os.path.join(subdir, filename))
            exif_dict = piexif.load(os.path.join(subdir, filename))
            new_date = datetime(int(date_pieces[0]), int(date_pieces[1]), int(date_pieces[2]), 0, 0, 0).strftime("%Y:%m:%d %H:%M:%S")
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, os.path.join(subdir, filename))
        else:
            print ('Skipping: %s' % filename)


#!/usr/bin/env python

from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import sys
import os
import pandas as pd

file0 = sys.argv[1]

image_list = []

with os.scandir(file0) as entries:
    for entry in entries:
        image_list.append(entry.name)
      
cols = ['name']
df = pd.DataFrame(image_list, columns = cols)
  


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging
    
def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
    return (lat,lon)


df['exif'] = df['name'].apply(get_exif)
df['geotags'] = df['exif'].apply(get_geotagging)
df['coords'] = df['geotags'].apply(get_coordinates)

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="test_app")
df['location'] = df['coords'].apply(geolocator.reverse)
#print(df['location'].raw['display_name'])
print(df['location'])
#df.to_csv('file.csv')



























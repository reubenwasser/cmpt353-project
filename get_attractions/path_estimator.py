
#Path Estimator Module
#Takes 2 input in the following order: (1) folder containing pictures (2) csv output file of exif_pictures.py

import sys
import os
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime




#function returns a dictionary with numeric keys that correspond to various types of data attached to the picture
#Adapted from: https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3
def get_exif(filename):
    path = sys.argv[1]
    image = Image.open(os.path.abspath(path + "/" + filename))
    image.verify()
    return image._getexif()


 
#function to extract the date and time the picture was taken
#Adapted from: https://orthallelous.wordpress.com/2015/04/19/extracting-date-and-time-from-images-with-python/
def get_datetime(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")
        
    std_fmt = '%Y:%m:%d %H:%M:%S.%f'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
 
    for t in tags:
        dat = exif.get(t[0])
        sub = exif.get(t[1], 0)
 
        # PIL.PILLOW_VERSION >= 3.0 returns a tuple
        dat = dat[0] if type(dat) == tuple else dat
        sub = sub[0] if type(sub) == tuple else sub
        if dat != None: break
 
    if dat == None: return None
    full = '{}.{}'.format(dat, sub)
    T = datetime.strptime(full, std_fmt)
    #T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
    return T


    

def path_estimator(image_file, location_file):
    #get folder containing all the pictures
    # image_file = sys.argv[1]
    
    #get csv file (output of exif_pictures.py) containing locations of the images
    #location_file = sys.argv[2]
    locations = pd.read_csv(location_file)
    locations = locations[['name','lat','lon','location']]
    # print(locations.info())
    
    #create empty list which will contain the filename of all the pictures
    image_list = [] 
    
    #get filename of every image in the directory and add it to the list
    with os.scandir(image_file) as entries:
        for entry in entries:
            image_list.append(entry.name)
    
    #build a dataframe with first column being the filename of the pictures
    images_df = pd.DataFrame(image_list, columns= ['name'])
    
    #get exif metadata of every image and add it to the dataframe
    images_df['exif'] = images_df['name'].apply(get_exif)
    
    #get datetime of every image and add it to the dataframe
    images_df['datetime']= images_df['exif'].apply(get_datetime)
   
    #join locations data to the images_df on name column
    joined_data = images_df.join(locations.set_index('name'),on = 'name')
    joined_data.to_csv('./get_attractions/results/joined_data.csv')
    
    #sort the pictures based on order of time taken
    #this would give us the path taken by the user, 
    #or more precisely the sequential order in which the locations were visited
    sorted_images = joined_data.sort_values(by=['datetime'])
    
    #print(sorted_images)
    
    sorted_images.to_csv('./get_attractions/results/sorted_images.csv')
    
    
    
'''
Note to self (possible to do): 
for those pictures that do not have a timestamp but have a location..maybe we can use 
some clever heuristic to estimate where it would fall in the sequence of locations visited....?

'''

# if __name__ == '__main__':
#     main()

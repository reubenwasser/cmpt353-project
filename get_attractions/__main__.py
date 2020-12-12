import sys
from .exif_pictures import exif_pictures
from .path_estimator import path_estimator
from .recommendations import recommendations
from .map import map_locations

def main():
    
    args = sys.argv[1:]
    
    for arg in args:
        print('passed folder - {}'.format(arg))

    exif_pictures(arg)
    path_estimator(arg, "./get_attractions/results/image_locations.csv")
    recommendations()
    map_locations("./get_attractions/results/sorted_images.csv")

if __name__ == '__main__':
    main()

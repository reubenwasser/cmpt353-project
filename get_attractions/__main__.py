import sys
from .exif_pictures import exif_pictures
from .path_estimator import path_estimator
from .recommendations import recommendations

def main():
    print('in main')
    args = sys.argv[1:]
    print('count of args :: {}'.format(len(args)))
    for arg in args:
        print('passed argument :: {}'.format(arg))

    exif_pictures(arg)
    path_estimator(arg, "./get_attractions/results/image_locations.csv")
    recommendations()


    # my_function('hello world')

    # my_object = MyClass('Thomas')
    # my_object.say_name()

if __name__ == '__main__':
    main()

from os import listdir
from os.path import isfile, join
import cv2 as cv


RESOURCES_FOLDER = 'resources'


class Image:
    def __init__(self, name):
        self._img = cv.imread(RESOURCES_FOLDER + '\\' + name, 0)
        self._w, self._h = self._img.shape[::-1]


imageNames = [f for f in listdir('resources') if isfile(join('resources', f))]
images = dict(zip([imn[:-4] for imn in imageNames], [Image(n) for n in imageNames]))

from glob import glob
from PIL import Image
import os
jpgs = glob('C:/Users/fuqiq/Downloads/Sreshta/*.jpg')

for j in jpgs:
    img = Image.open(j)
    img.save(j[:-3] + 'png')
    os.remove(j)

from glob import glob
from PIL import Image
import os
import numpy as np
from skimage.util import random_noise

pngs = glob('C:/CourseWork/CSE 546 Cloud Computing/Projects/Project2/Models/data/real_4/*/*/*.png')


def add_salt_and_pepper(image, amount):
    output = np.copy(np.array(image))

    # add salt
    nb_salt = np.ceil(amount * output.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(nb_salt)) for i in output.shape]
    output[coords] = 1

    # add pepper
    nb_pepper = np.ceil(amount * output.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(nb_pepper)) for i in output.shape]
    output[coords] = 0

    return Image.fromarray(output)


for p in pngs:
    img = Image.open(p)
    outimg = add_salt_and_pepper(img, .05)
    outimg.save(p[:-4] + '_gau.png')
    # os.remove(j)

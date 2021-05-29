import numpy as np
from skimage.transform import resize
from PIL import Image

def data_preprocessing(image):
    new_image = np.zeros((100,400))
    for  idx1,val1 in enumerate(image):
        for idx2,val2 in enumerate(val1):
            if np.sum(val2) > 0:
                new_image[idx1][idx2] = 1
            else:
                new_image[idx1][idx2] = 0
    start = 400
    end = 0
    for height in new_image:
        for idx, val in enumerate(height):
            if val != 0:
                if start > idx:
                    start = idx
                    break
        height = np.flip(height)
        for idx,val in enumerate(height):
            if val != 0:
                if end < (399- idx):
                    end = 399 - idx
                    break
    img = Image.fromarray(new_image)
    area = (start-3,0,end+3,100)
    crp = img.crop(area)
    img = np.array(crp)
    tmpIMG = resize(img, (200,64))
    data = tmpIMG.reshape(1, tmpIMG.shape[0], tmpIMG.shape[1], 1)


    return data
import os
import numpy as np
from PIL import Image
from Music_function import image_Augmentation

'''
image_Augmentation(image,'d_sn_resized', 100)
늘리고 싶은 이미지, 파일 이름, 이미지 생성 개수
를 넣으면 파일에 이미지를 생성한다!
'''

path_dir = r'output'
file_list = os.listdir(path_dir)
print(file_list)

d_sn_resized = []
for name in file_list:
    png_name = path_dir + '/' + name
    image = Image.open(png_name)
    arr = np.array(image)
    d_sn_resized.append(arr)

np.save('d_sn_resized.npy', np.array(d_sn_resized))

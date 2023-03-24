
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

import sys
import shutil

path=r'C:\Users\FYC\Desktop\TNSCUI2020_train\TNSCUI2020_train\mask/'
newpath=r'C:\Users\FYC\Desktop\TNSCUI2020_train\TNSCUI2020_train\24MASK/'
def turnto24(path):
   files = os.listdir(path)
   files = np.sort(files)
   i = 0
   for f in files:
       imgpath = path + f
       img = Image.open(imgpath).convert('RGB')
       dirpath = newpath
       file_name, file_extend = os.path.splitext(f)
       dst = os.path.join(os.path.abspath(dirpath), file_name + '.PNG')
       img.save(dst)

turnto24(path)




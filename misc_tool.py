import os
from os import listdir
import numpy as np
def mkdir(tar_path):
    try:
        if os.path.isdir(tar_path)==False:
            os.makedirs(tar_path)
        else:
            print('The folder already existed')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def count_subfolder(tar_path):
    fol=[f for f in listdir(tar_path) if os.path.isdir(os.path.join(tar_path, f)) ]

    return np.size(fol)

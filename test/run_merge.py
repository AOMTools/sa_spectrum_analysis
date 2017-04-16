import sys
import os
sys.path.append('/home/chihuan/research/programs/python/data_analysis/sa_spectrum')
import merge as mg
tar_path=os.getcwd()
print(tar_path)
mg.merge(tar_path=tar_path)

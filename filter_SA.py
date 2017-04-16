import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import processor as ps
import misc_tool as mt
#load verdict_report
def filter(tar_path):
    verdict_path=tar_path+'/verdict_report/'
    #tar_path: location of merge_norm/T
    tar_pathT=tar_path+'/merge_norm/T/'
    tar_pathF=tar_path+'/merge_norm/F/'
    tar_pathR=tar_path+'/merge_norm/R/'
    verdict_file= [f for f in listdir(verdict_path) if isfile(join(verdict_path, f)) ]
    verdict_file.sort()
    for f in verdict_file:
        T_sa=[]#Transmission of selected single atom
        R_sa=[]
        F_sa=[]

        T_nsa=[]#Transmission of other cases
        R_nsa=[]
        F_nsa=[]



        verdict_report=verdict_path+f
        tar_pathTraw=tar_pathT+f
        tar_pathRraw=tar_pathR+f
        tar_pathFraw=tar_pathF+f

        raw_T=np.genfromtxt(tar_pathTraw)[1:]
        raw_R=np.genfromtxt(tar_pathRraw)[1:]
        raw_F=np.genfromtxt(tar_pathFraw)[1:]

        (masked_id_T,masked_array_T)=ps.mask(raw_T,verdict_report=verdict_report)
        (masked_id_R,masked_array_R)=ps.mask(raw_R,verdict_report=verdict_report)
        (masked_id_F,masked_array_F)=ps.mask(raw_F,verdict_report=verdict_report)

        (masked_id_nsa_T,masked_array_nsa_T)=ps.mask(raw_T,case='MA/UC',verdict_report=verdict_report)
        (masked_id_nsa_R,masked_array_nsa_R)=ps.mask(raw_R,case='MA/UC',verdict_report=verdict_report)
        (masked_id_nsa_F,masked_array_nsa_F)=ps.mask(raw_F,case='MA/UC',verdict_report=verdict_report)


        T_sa.append(np.genfromtxt(tar_pathTraw)[0])#1st row is time
        R_sa.append(np.genfromtxt(tar_pathRraw)[0])#1st row is time
        F_sa.append(np.genfromtxt(tar_pathFraw)[0])#1st row is time

        T_nsa.append(np.genfromtxt(tar_pathTraw)[0])#1st row is time
        R_nsa.append(np.genfromtxt(tar_pathRraw)[0])#1st row is time
        F_nsa.append(np.genfromtxt(tar_pathFraw)[0])#1st row is time


        for a in masked_array_T:
            T_sa.append(a)
        for a in masked_array_R:
            R_sa.append(a)
        for a in masked_array_F:
            F_sa.append(a)
        for a in masked_array_nsa_T:
            T_nsa.append(a)
        for a in masked_array_nsa_R:
            R_nsa.append(a)
        for a in masked_array_nsa_F:
            F_nsa.append(a)

        mt.mkdir(tar_path+'/merge_norm_sa/T/')
        mt.mkdir(tar_path+'/merge_norm_sa/F/')
        mt.mkdir(tar_path+'/merge_norm_sa/R/')
        mt.mkdir(tar_path+'/merge_norm_nsa/T/')
        mt.mkdir(tar_path+'/merge_norm_nsa/F/')
        mt.mkdir(tar_path+'/merge_norm_nsa/R/')

        output_pathT='merge_norm_sa/T/'+f
        print(output_pathT)

        np.savetxt(output_pathT,T_sa)
        print('size of T_sa')
        print(np.shape(T_sa))

        output_pathF='merge_norm_sa/F/'+f
        print(output_pathF)
        np.savetxt(output_pathF,F_sa)
        print('size of F_sa')
        print(np.shape(F_sa))

        output_pathR='merge_norm_sa/R/'+f
        print(output_pathR)
        np.savetxt(output_pathR,R_sa)
        print('size of R_sa')
        print(np.shape(R_sa))

        output_pathT_nsa='merge_norm_nsa/T/'+f
        print(output_pathT_nsa)
        np.savetxt(output_pathT_nsa,T_nsa)
        print('size of T_nsa')
        print(np.shape(T_nsa))

        output_pathR_nsa='merge_norm_nsa/R/'+f
        print(output_pathR_nsa)
        np.savetxt(output_pathR_nsa,R_nsa)
        print('size of R_nsa')
        print(np.shape(R_nsa))

        output_pathF_nsa='merge_norm_nsa/F/'+f
        print(output_pathF_nsa)
        np.savetxt(output_pathF_nsa,F_nsa)
        print('size of F_nsa')
        print(np.shape(F_nsa))

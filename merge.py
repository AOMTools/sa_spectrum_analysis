import numpy as np
import sys
import os
import matplotlib.pyplot as plt

def merge(tar_path,num_avg=-1):
    #num_avg=-1: number of sets to average. -1:take all. must be larger than 1
    #cwd = os.getcwd()
    #tar_path=cwd+'/data'
    tar_path2=tar_path+'/data'
    folder2 = [f for f in os.listdir(tar_path2) if (os.path.isdir(os.path.join(tar_path2, f)) and f[0]=='2') ]
    folder2.sort()
    folder=[]
    if num_avg==-1:
        folder=folder2
    elif num_avg==1:
        folder.append(folder2[0])
    else:
        folder=folder2[0:num_avg]

    ###get list of freq
    folder0=folder[0]
    tar_path0=tar_path2+'/'+folder0
    freqf = [f for f in os.listdir(tar_path0) if (os.path.isdir(os.path.join(tar_path0, f)) and f[0]!='e' )]
    #########################

    ###Make output folders
    output_path='merge_norm'
    T_output_path=tar_path+'/'+output_path+'/'+'T'
    R_output_path=tar_path+'/'+output_path+'/'+'R'
    F_output_path=tar_path+'/'+output_path+'/'+'F'
    print(T_output_path)

    try:
        if os.path.isdir(T_output_path)==False:
            os.makedirs(T_output_path)
        if os.path.isdir(R_output_path)==False:
            os.makedirs(R_output_path)
        if os.path.isdir(F_output_path)==False:
            os.makedirs(F_output_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    ##############################


    #Extract time array
    rawpathT=tar_path0+'/'+'384'+'/'+'raw_T'
    rawpathF=tar_path0+'/'+'384'+'/'+'raw_F'
    timeT=np.genfromtxt(rawpathT)[0,:]
    timeF=np.genfromtxt(rawpathF)[0,:]
    '''
    print('time array for T')
    print(timeT)
    print(np.shape(timeT))
    print('time array for F')
    print(timeF)
    '''
    #######################
    #Normalize Tranmission (raw_T) of each freq set with it's emptycav value at that freq
    freqf.sort()
    for j,freqname in enumerate(freqf):
        normT=[]
        normR=[]
        mergeF=[]
        #add time as the first row
        normT.append(timeT)
        normR.append(timeT)
        mergeF.append(timeF)
        print('Going through freq ',freqname)
        for i,setname in enumerate(folder):
            print('Going through folder ',setname)
            emptycav_path=tar_path2+'/'+setname+'/'+'emptycavspec.dat'
            emptycavspec=np.genfromtxt(emptycav_path)
            #maxT=emptycavspec[12,1]
            #maxR=emptycavspec[0,3]
            Remptyspec=emptycavspec[:,3]
            stdRemptyspec=emptycavspec[:,4]
            Temptyspec=emptycavspec[:,1]

            stdTemptyspec=emptycavspec[:,2]
            tar_pathd=tar_path2+'/'+setname


            rawpath=tar_pathd+'/'+freqname+'/'+'raw_T'
            rawpathR=tar_pathd+'/'+freqname+'/'+'raw_R'
            rawpathF=tar_pathd+'/'+freqname+'/'+'raw_F'
            #dataT=np.genfromtxt(rawpath)[1:,:]/0.97/Temptyspec[j]*30#the first row is time

            dataT=np.genfromtxt(rawpath)[1:,:]/0.97#the first row is time
            dataR=np.genfromtxt(rawpathR)[1:,:]/0.97
            dataF=np.genfromtxt(rawpathF)[1:,:]/0.97
            #print('shape of dataT')
            print(np.shape(np.genfromtxt(rawpath)[1:,:]))
            #print('shape of dataF')
            #print(np.shape(dataF))
            for a in dataT:
                normT.append(a)
            for a in dataF:
                mergeF.append(a)
            for a in dataR:
                normR.append(a)
            #print(mergeF)


        fnameT=T_output_path+'/'+str(freqname)+'.dat'
        np.savetxt(fnameT,normT)
        fnameF=F_output_path+'/'+str(freqname)+'.dat'
        np.savetxt(fnameF,mergeF)
        fnameR=R_output_path+'/'+str(freqname)+'.dat'
        np.savetxt(fnameR,normR)

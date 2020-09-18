#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:57:58 2018

@author: nephilim
"""
from multiprocessing import Pool
import numpy as np
import Add_CPML
import Time_loop
import Wavelet
from matplotlib import pyplot,cm
import time
import shutil
import os
import scipy.io as scio


def Forward2D(parameter,value_source,value_receiver,index):
    t=np.arange(parameter['k_max'])*parameter['dt']
    f=Wavelet.ricker(t,parameter['Freq'])
    CPML_Params=Add_CPML.Add_CPML(parameter['xl'],parameter['zl'],parameter['sigma'],\
                                  parameter['epsilon'],parameter['mu'],parameter['dx'],parameter['dz'],parameter['dt'])
    Forward_data=Time_loop.time_loop(parameter['xl'],parameter['zl'],parameter['dx'],parameter['dz'],\
                                     parameter['dt'],parameter['sigma'],parameter['epsilon'],parameter['mu'],\
                                     CPML_Params,f,parameter['k_max'],value_source,value_receiver)
    Profile=np.empty((parameter['k_max']))
    for i in range(parameter['k_max']):
        tmp=Forward_data.__next__()
        Profile[i]=tmp[0]
    return index,Profile
    
def Forward_2D(parameter):
    pool=Pool(processes=8)
    Profile=np.empty((parameter['k_max'],len(parameter['SourcePosition'])))
    res_l=[]
    for idx,data_position in enumerate(zip(parameter['SourcePosition'],parameter['ReceiverPosition'])):
        # print(data_position[0])
        # print(data_position[1])
        res=pool.apply_async(Forward2D,args=(parameter,data_position[0],data_position[1],idx))
        res_l.append(res)
    pool.close()
    pool.join()
    for res in res_l:
        result=res.get()
        Profile[:,result[0]]=result[1]
        del result
    del res_l
    pool.terminate()
    return Profile
    
    
    
    
if __name__=='__main__':
    #Create Folder
    if not os.path.exists('./ProfileLT'):
        os.makedirs('./ProfileLT')
    else:
        shutil.rmtree('./ProfileLT')
        os.makedirs('./ProfileLT')
    startTime=time.time()
    parameter=dict()
    parameter['xl']=150
    parameter['zl']=800
    parameter['dx']=0.005
    parameter['dz']=0.005
    parameter['dt']=1e-11
    parameter['k_max']=5000
    parameter['Freq']=9e8
    
    
    data_epsilon=scio.loadmat('./epsilon1.mat')['epsilon1'].astype('float')
    # data_epsilon=10*np.ones((parameter['xl'],parameter['zl']))
    # data_epsilon[:40,:]=4
    # for idx_x in range(parameter['xl']):
    #     for idx_z in range(parameter['zl']):
    #         if (110-idx_z*0.1)<idx_x:
    #             data_epsilon[idx_x,idx_z]=4
            
    # for idx_x in range(parameter['xl']):
    #     for idx_z in range(parameter['zl']):
    #         if (150+idx_z*0.1)<idx_x:
    #             data_epsilon[idx_x,idx_z]=8
    
    data_sigma=scio.loadmat('./sigma1.mat')['sigma1']
    # data_sigma[:40,:]=0.001
    # for idx_x in range(parameter['xl']):
    #     for idx_z in range(parameter['zl']):
    #         if (110-idx_z*0.1)<idx_x:
    #             data_sigma[idx_x,idx_z]=1e-4
            
    # for idx_x in range(parameter['xl']):
    #     for idx_z in range(parameter['zl']):
    #         if (150+idx_z*0.1)<idx_x:
    #             data_sigma[idx_x,idx_z]=1e-4
            
    parameter['sigma']=data_sigma
    parameter['epsilon']=data_epsilon
    parameter['mu']=np.ones((parameter['epsilon'].shape))
    step=0
    z_Position=np.arange(10+step,parameter['zl']-10,2)
    x_Position=(np.ones(z_Position.shape)*10).astype(int)
    parameter['SourcePosition']=[(x_Position[idx],z_Position[idx]-step) for idx in range(len(x_Position))]
    parameter['ReceiverPosition']=[(x_Position[idx],z_Position[idx]) for idx in range(len(x_Position))]
    Profile=Forward_2D(parameter)
    print('Forward Done! Elapsed time is %s s'%(time.time()-startTime))
    # np.save('sigma.npy',parameter['sigma'])
    # np.save('epsilon.npy',parameter['epsilon'])
    # np.save('ProfileClean.npy',Profile)
    # np.save('sigma.npy',parameter['sigma'])
    



    
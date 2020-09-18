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
import CreateRandomModel
from matplotlib import pyplot,cm
import time
import shutil
import os


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
    if not os.path.exists('./Profile_test'):
        os.makedirs('./Profile_test')
    else:
        shutil.rmtree('./Profile_test')
        os.makedirs('./Profile_test')
    startTime=time.time()
    parameter=dict()
    parameter['xl']=100
    parameter['zl']=200
    parameter['dx']=0.025
    parameter['dz']=0.025
    parameter['dt']=1e-11
    parameter['k_max']=7000
    parameter['Freq']=4e8
    
    parameter['sigma']=np.load('sigma_complex.npy')
    # parameter['epsilon']=np.load('epsilon.npy')
    
    epsilon_data=np.load('epsilon_complex.npy')
    epsilon_random=CreateRandomModel.RandomModel(parameter['zl'],parameter['xl'],1,1,0.2)
    epsilon_data[epsilon_data==9]=epsilon_random[epsilon_data==9]*9
    epsilon_data[epsilon_data==7]=epsilon_random[epsilon_data==7]*7
    parameter['epsilon']=epsilon_data
    
    parameter['mu']=np.ones((parameter['epsilon'].shape))
    step=4
    x_Position=(np.ones(parameter['zl']-20-step)*10).astype(int)
    z_Position=np.arange(10+step,parameter['zl']-10)
    parameter['SourcePosition']=[(x_Position[idx],z_Position[idx]-step) for idx in range(len(x_Position))]
    parameter['ReceiverPosition']=[(x_Position[idx],z_Position[idx]) for idx in range(len(x_Position))]
    Profile=Forward_2D(parameter)
    print('Forward Done! Elapsed time is %s s'%(time.time()-startTime))
    np.save('ComplexProfileStochastic.npy',Profile)
    
    pyplot.figure(1)
    pyplot.imshow(epsilon_data,vmin=1,vmax=20,extent=(0,2,1,0),cmap=cm.seismic)
            # pyplot.figure(2)
            # pyplot.imshow(Profile,extent=(0,1,0,1))

    
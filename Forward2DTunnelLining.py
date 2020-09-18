#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:05:54 2020

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
# import CreateTunnelLining
import StochasticModel



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
    if not os.path.exists('./Profile_TunnelLining'):
        os.makedirs('./Profile_TunnelLining')
    else:
        shutil.rmtree('./Profile_TunnelLining')
        os.makedirs('./Profile_TunnelLining')
    startTime=time.time()
    parameter=dict()
    parameter['xl']=100
    parameter['zl']=200
    parameter['dx']=0.005
    parameter['dz']=0.005
    parameter['dt']=5e-12
    parameter['k_max']=5000
    parameter['Freq']=9e8
    for iteration in range(1):
        # Pipe_row=[20,24,18,22,24,22]+[55,55,71,71]+[70,70,84,84]
        # PiPe_column=[8,43,83,125,169,196]+[14,25,140,150]+[14,25,140,150]
        # row_random0=list(np.random.randint(low=15,high=25,size=6))
        # row_random1=list(np.random.randint(low=70,high=80,size=1))*2
        # row_random2=list(np.random.randint(low=80,high=90,size=1))*2
        # column_random0=list(np.random.randint(low=8,high=196,size=6))
        # column_random1=list(np.random.randint(low=140,high=160,size=2))
        # column_random2=list(np.random.randint(low=140,high=160,size=2))
        # Pipe_row=[20,24,18,22,24,22]+[71,71]+[84,84]
        # PiPe_column=[8,43,83,125,169,196]+[140,150]+[140,150]
        # Pipe_row=row_random0+row_random1+row_random2
        # PiPe_column=column_random0+column_random1+column_random2
        # Pipe_position=np.column_stack((Pipe_row,PiPe_column))
        
        # sigma_data=np.zeros((100,200))
        # epsilon_data=7*np.ones((100,200))
        Stochastic_epsilon,NoStochastic_epsilon=StochasticModel.StochasticToCreateModel(parameter)
        StochasticModel.ChooseModel(parameter,Stochastic_epsilon,NoStochastic_epsilon,1)

        # left_column=[37,72,112,167]
        # bottom_row=[70,57,60,64]
        # left_column=[90,37]
        # bottom_row=[57,70]
        # left_column=list(np.random.randint(low=35,high=90,size=2))
        # bottom_row=list(np.random.randint(low=50,high=70,size=2))
        
        
        # width=len(left_column)*[4,]
        # high=len(left_column)*[12,]
        # param=np.column_stack((left_column,bottom_row,width,high))
        # CreateTunnelLining.tunnel_lining(epsilon_data,sigma_data,Pipe_position,param,np.random.randint(low=30,high=40))
        # parameter['epsilon']=epsilon_data
        # parameter['sigma']=sigma_data
        
        
        # parameter['mu']=np.ones((parameter['epsilon'].shape))
        step=0
        x_Position=(np.ones(parameter['zl']-20-step)*10).astype(int)
        z_Position=np.arange(10+step,parameter['zl']-10)
        parameter['SourcePosition']=[(x_Position[idx],z_Position[idx]-step) for idx in range(len(x_Position))]
        parameter['ReceiverPosition']=[(x_Position[idx],z_Position[idx]) for idx in range(len(x_Position))]
        Profile=Forward_2D(parameter)
        print('Forward Done! Elapsed time is %s s'%(time.time()-startTime))
        np.save('./Profile_TunnelLining/TunnelLining_Iter_%s_%s.npy'%(iteration,1),Profile)
        import scipy.io as scio
        StochasticData=np.load('./Profile_TunnelLining/TunnelLining_Iter_0_1.npy')
        scio.savemat('StochasticData.mat',{'profile':StochasticData})
        # pyplot.imshow(Profile,extent=(0,1,0,1),vmax=0.5*np.max(Profile),vmin=0.5*np.min(Profile),cmap=cm.seismic)
        # StochasticModel.ChooseModel(parameter,Stochastic_epsilon,NoStochastic_epsilon,0)
        # Profile=Forward_2D(parameter)
        # print('Forward Done! Elapsed time is %s s'%(time.time()-startTime))
        # np.save('./Profile_TunnelLining/TunnelLining_Iter_%s_ %s.npy'%(iteration,0),Profile)
    
    
    
    
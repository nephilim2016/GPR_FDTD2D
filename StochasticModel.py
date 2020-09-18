#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 14:44:51 2020

@author: nephilim
"""
import numpy as np
import CreateRandomModel
import CreateTunnelLining
from matplotlib import pyplot

def ChooseModel(parameter,Stochastic_epsilon,NoStochastic_epsilon,compare):
    if compare:
        parameter['epsilon']=Stochastic_epsilon
        parameter['sigma']=np.zeros(Stochastic_epsilon.shape)
        parameter['mu']=np.ones((parameter['epsilon'].shape))
    else:
        parameter['epsilon']=NoStochastic_epsilon
        parameter['sigma']=np.zeros(Stochastic_epsilon.shape)
        parameter['mu']=np.ones((parameter['epsilon'].shape))
        
    
def StochasticToCreateModel(parameter):
    # Pipe_row=[20,24,18,22,24,22]+[55,55,71,71]+[70,70,84,84]
    # PiPe_column=[8,43,83,125,169,196]+[14,25,140,150]+[14,25,140,150]
    row_random0=list(np.random.randint(low=20,high=25,size=6))
    row_random1=list(np.random.randint(low=100,high=115,size=1))*2
    row_random2=list(np.random.randint(low=100,high=123,size=1))*2
    column_random0=list(np.random.randint(low=20,high=170,size=6))
    column_random1=list(np.random.randint(low=20,high=30,size=2))
    column_random2=list(np.random.randint(low=20,high=30,size=2))
    # Pipe_row=[20,24,18,22,24,22]+[71,71]+[84,84]
    # PiPe_column=[8,43,83,125,169,196]+[140,150]+[140,150]
    Pipe_row=row_random0+row_random1+row_random2
    PiPe_column=column_random0+column_random1+column_random2
    Pipe_position=np.column_stack((Pipe_row,PiPe_column))
        
    sigma_data=np.zeros((parameter['xl'],parameter['zl']))
    epsilon_data_random=CreateRandomModel.RandomModel(parameter['zl'],parameter['xl'],5,5,0.5)
    epsilon_data=7*np.ones((parameter['xl'],parameter['zl']))
    
    # left_column=[37,72,112,167]
    # bottom_row=[70,57,60,64]
    # left_column=[90,37]
    # bottom_row=[57,70]
    left_column=list(np.random.randint(low=40,high=140,size=3))
    bottom_row=list(np.random.randint(low=90,high=130,size=3))
    
    
    width=len(left_column)*[4,]
    high=len(left_column)*[12,]
    param=np.column_stack((left_column,bottom_row,width,high))
    CreateTunnelLining.tunnel_lining(epsilon_data,sigma_data,Pipe_position,param,60)
    NoStochastic_epsilon=epsilon_data
    Stochastic_epsilon=epsilon_data.copy()
    Stochastic_epsilon[Stochastic_epsilon==7]=7*epsilon_data_random[Stochastic_epsilon==7]
    # parameter['epsilon']=epsilon_data
    # parameter['sigma']=sigma_data
        
        
    # parameter['mu']=np.ones((parameter['epsilon'].shape))
    
    
    return Stochastic_epsilon,NoStochastic_epsilon

            
    
    # pyplot.figure(1)
    # pyplot.imshow(parameter['epsilon'])
    
def AddCircle(parameter,stochastic,data,Iter):
    for iteration in range(Iter):
        Stochastic_epsilon_set=[1,10,15,81]
        index=np.random.randint(0,4)
        Stochastic_epsilon=Stochastic_epsilon_set[index]
        r=np.random.randint(10,30)
        point_x=np.random.randint(20+r,70)
        point_z=np.random.randint(10+r,parameter['zl']-10-r)
        print('(%s,%s),radium=%s\n'%(point_x,point_z,r))
        for idx_x in range(parameter['xl']):
            for idx_z in range(parameter['zl']):
                if (idx_x-point_x)**2+(idx_z-point_z)**2<=r**2:
                    data[idx_x,idx_z]=Stochastic_epsilon
                    stochastic[idx_x,idx_z]=Stochastic_epsilon
    return Iter
                    
def AddRectangle(parameter,stochastic,data,Iter):
    for iteration in range(Iter):
        Stochastic_epsilon_set=[1,10,15,81]
        index=np.random.randint(0,4)
        Stochastic_epsilon=Stochastic_epsilon_set[index]
        width=np.random.randint(10,70)
        high=np.random.randint(10,40)
        point_x=np.random.randint(10+high,parameter['xl']-high)
        point_z=np.random.randint(10+width,parameter['zl']-10-width)
        print('(%s,%s),high=%s,width=%s\n'%(point_x,point_z,high,width))
        stochastic[point_x:point_x+high,point_z:point_z+width]=Stochastic_epsilon
        data[point_x:point_x+high,point_z:point_z+width]=Stochastic_epsilon
    return Iter

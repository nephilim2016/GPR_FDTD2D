#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:30:25 2020

@author: nephilim
"""
import numpy as np
from numba import jit

@jit(nopython=True)
def tunnel_lining(epsilon,sigma,Rebar,param_Rec,row_position):

    for idx in range(Rebar.shape[0]):
        for index_row in range(epsilon.shape[0]):
            for index_column in range(epsilon.shape[1]):
                if (index_row-Rebar[idx,0])**2+(index_column-Rebar[idx,1])**2<=4:
                    epsilon[index_row,index_column]=1
                    sigma[index_row,index_column]=1e6

    epsilon[row_position:row_position+3,:]=2.1
    sigma[row_position:row_position+3,:]=0
    
    # for index_row in range(epsilon.shape[0]):
    #         for index_column in range(epsilon.shape[1]):
    #             if (index_row-60)**2+(index_column-50)**2<=81:
    #                 epsilon[index_row,index_column]=1
    #                 sigma[index_row,index_column]=0
    # epsilon[70:80,120:170]=1
    # sigma[70:80,120:170]=0
    for idx in range(param_Rec.shape[0]):
        epsilon[param_Rec[idx,1]-2:param_Rec[idx,1],param_Rec[idx,0]-3:param_Rec[idx,0]+param_Rec[idx,2]+3]=1
        epsilon[param_Rec[idx,1]:param_Rec[idx,1]+param_Rec[idx,3],param_Rec[idx,0]:param_Rec[idx,0]+param_Rec[idx,2]]=1
        epsilon[param_Rec[idx,1]+param_Rec[idx,3]:param_Rec[idx,1]+param_Rec[idx,3]+2,param_Rec[idx,0]-3:param_Rec[idx,0]+param_Rec[idx,2]+3]=1
        
        sigma[param_Rec[idx,1]-2:param_Rec[idx,1],param_Rec[idx,0]-3:param_Rec[idx,0]+param_Rec[idx,2]+3]=1e6
        sigma[param_Rec[idx,1]:param_Rec[idx,1]+param_Rec[idx,3],param_Rec[idx,0]:param_Rec[idx,0]+param_Rec[idx,2]]=1e6
        sigma[param_Rec[idx,1]+param_Rec[idx,3]:param_Rec[idx,1]+param_Rec[idx,3]+2,param_Rec[idx,0]-3:param_Rec[idx,0]+param_Rec[idx,2]+3]=1e6
        
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 16:36:47 2020

@author: nephilim
"""
import numpy as np
def DataNormalized(Data):
    MinData=np.min(Data)
    Data-=MinData
    MaxData=np.max(Data)
    Data/=MaxData
    return Data*255

def InverseDataNormalized(Data,NormalData):
    MinData=np.min(Data)
    MaxData=np.max(Data)
    Factor=MaxData-MinData
    InverseData=NormalData*Factor/255+MinData
    return InverseData
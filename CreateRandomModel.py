#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 23:24:38 2020

@author: nephilim
"""

import numpy as np
import scipy as sp
from matplotlib import pyplot,cm

def RandomModel(x_len,z_len,a,b,epsilon):
    A=np.linspace(0,1000,x_len)
    x=np.dot(np.ones((z_len,1)),A.reshape((1,-1)))
    B=np.linspace(0,1000,z_len)
    y=np.dot(np.ones((x_len,1)),B.reshape((1,-1)))
    y=y.T
    r=0.4
    f=np.exp(-((x/a)**2+(y/b)**2)**(1/(1+r)))
    F=sp.fft.fft2(f)
    fai=np.random.uniform(0,2*np.pi,F.shape)
    F1=np.abs(F)*np.exp(complex(0,1)*fai)
    z=np.fft.ifft2(F1)
    zz=np.imag(z)
    miu=np.mean(zz)
    zz2=zz.ravel(order='F')
    d=np.var(zz2)
    sigma=(epsilon/d)*(zz-miu)
    v0=2000
    v1=v0*(1+sigma)/1000
    random_=(v1/1000+1)
    return random_

if __name__=='__main__':
    data=RandomModel(300,300,5,5,0.2)
    print(np.max(data))
    print(np.min(data))
    pyplot.imshow(data,cmap=cm.seismic)
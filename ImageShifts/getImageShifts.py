# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 17:06:17 2020

@author: haywoojr
"""

import numpy as np
import struct
import binascii

#converts the Hex Value transformation Matrix into numpy matrix
def transformationToMatrix(num):
    block_size = 16
    values = []
    #removed the num[2:] below because it is not needed based on how the data
    #is sent
    #num = num[2:]
    for i in range(0,len(num),block_size):
        values.append(struct.unpack('<d',binascii.unhexlify(num[i:i+block_size])))
    m = np.concatenate((np.array(values).reshape((4,3)), np.array([0,0,0,1]).reshape((4,1))),axis=1)
    m = np.transpose(m)
    #print(m)
    return m

def getImageShifts(transHex,iso_X,iso_Y,iso_Z):
    #transHex should be passed in
    #transHex is the value from the transformation column in the database
    mat=transformationToMatrix(transHex)
    #inverse converts the dicom transformation matrix to "iec" coordinates
    #see https://doi.org/10.1002/acm2.12348
    mat_inverse=np.linalg.inv(mat)
    #print(mat_inverse)
    
    #rotations can be calulated directly from the inverse matrix
    irot=-np.arcsin(mat_inverse[2,0])
    cosb=np.cos(irot)
    sina=mat_inverse[1,0]/cosb
    iroll=np.arcsin(sina)
    sinc=mat_inverse[2,1]/cosb
    ipitch=np.arcsin(sinc)
    #convert to degrees
    irot   *= 180.0/np.pi
    iroll  *= 180.0/np.pi
    ipitch *= 180.0/np.pi
    #for the TrueBeam running the isocenter through the transformation matrix
    #will return the shifts
    #does not work for iX
    #1 added to the end to make 4x1 array since transformation matrix is 4x4
    isoArray=np.array([iso_X,iso_Y,iso_Z,1])
    #get the couch shifts through matrix multiplication
    lat_shift,vrt_shift,lng_shift,fake_shift=np.matmul(mat_inverse,isoArray)
    #return the values as seen in the offline review workspace
    return np.array([vrt_shift,lng_shift,lat_shift,ipitch,iroll,irot])
    
    
    
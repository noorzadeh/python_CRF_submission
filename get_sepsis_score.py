#!/usr/bin/env python

import numpy as np
import pickle

def Interpolation(InMat):
    OutMat = np.zeros(InMat.shape, dtype=float)
    for i in range(InMat.shape[1]):
        Col = InMat[:,i]
        if (np.any(np.isnan(Col))):
            if (np.all(np.isnan(Col))):
                dd = 1
            else:
                # set all first nan values to the first non-nan value
                j = 0
                while (np.isnan(Col[j]) & (j<len(Col))):
                    j += 1
                Col[:j] = Col[j]
                
                # set all last nan values to the last non-nan value
                j = -1
                while (np.isnan(Col[j])) & (j>-len(Col)):
                    j -= 1
                Col[j:] = Col[j]
                
                # interpolate the other nan values
                if (np.any(np.isnan(Col))):
                    t = np.array(range(len(Col)))
                    NonNanCol = Col[~np.isnan(Col)]
                    NonNant = t[~np.isnan(Col)]
                    Nant = t[np.isnan(Col)]
                        
                    NanColInterp = np.interp(Nant, NonNant, NonNanCol)
                    Col[Nant] = NanColInterp
                OutMat[:,i] = Col
        else:
            OutMat[:,i] = Col
        
    return OutMat

def get_sepsis_score(data, model):
    
    ssvm = model['SSVMVar']
    cols = model['ColVar']
    Dmean = model['MeanVar']
    Dstd = model['StdVar']
	
    D = np.empty(1, dtype=object)
    
    dNormalOrig = data[:,cols]
    
    dNormal = Interpolation(dNormalOrig)
    
    DmeanMat = np.repeat(Dmean,len(dNormal),axis=0)
    DstdMat = np.repeat(Dstd,len(dNormal),axis=0)
    dNormal = np.nan_to_num((dNormal - DmeanMat) / DstdMat) 
    
    D[0] = dNormal 
    score = 0.5
    labelVec = ssvm.predict(D)
    label = labelVec[0][-1]
    if (label == 2):
        label = 1
    return score, label

def load_sepsis_model():
    ModelFileName = 'ChainCRF_Model.pkl'
    with open(ModelFileName, 'rb') as file:
        ssvm, cols, Dmean, Dstd = pickle.load(file, encoding='latin1')
    model = {'SSVMVar': ssvm,'ColVar': cols,'MeanVar': Dmean,'StdVar': Dstd}

    return model 

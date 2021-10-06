import numpy as np
import matplotlib as mp
mp.use('Agg')
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import os

interpolation='nearest'#'bilinear'#'nearest'

def loadData(data):
    weights = np.loadtxt(data)
    return(weights)

def reshapeFields(w):
    nbrPost,nbrPre = np.shape(w)
    fieldSize = int(np.sqrt(nbrPre/2))
    fields = np.zeros((nbrPost,fieldSize,fieldSize,2))
    for i in range(nbrPost):
        field = w[i,:]
        fields[i] = np.reshape(field,(fieldSize,fieldSize,2))
    return(fields)

def setSubplotDimension(a):
    x = 0
    y = 0
    if ( (a % 1) == 0.0):
        x = a
        y =a
    elif((a % 1) < 0.5):
        x = round(a) +1
        y = round(a)
    else :
        x = round(a)
        y = round(a)
    return (x,y)  


def plotONOFF(fields,data):
    name = data[0:data.index('_')]
    nbr = data[data.index('_')+1:]
    wMax = np.max(fields[:,:,:,0] - fields[:,:,:,1])
    wMin = np.min(fields[:,:,:,0] - fields[:,:,:,1])#0.0
    fig = plt.figure()
    x,y = setSubplotDimension(np.sqrt(np.shape(fields)[0]))
    for i in range(np.shape(fields)[0]):
        field = fields[i,:,:,0] - fields[i,:,:,1]
        plt.subplot(x,y,i+1)
        plt.axis('off')
        im = plt.imshow(field,cmap=mp.cm.Greys_r,aspect='auto',interpolation=interpolation,vmin=wMin,vmax=wMax)
        plt.axis('equal')
    fig.savefig('ONOFF/'+name+'_'+nbr+'ONOFF.png')
    print('On - Off finish')

def createDir():
    if not os.path.exists('ONOFF'):
        os.mkdir('ONOFF')

def plotWeightHist(files):
    weights = np.loadtxt('exitatory/V1weight_400000.txt')
    nbrPost,nbrPre = np.shape(weights)
    weights = np.reshape(weights,(nbrPost*nbrPre))
    plt.figure()
    plt.hist(weights,50)
    plt.savefig('weightHist.png')
    weights = np.loadtxt('V1toIN/V1toIN_400000.txt')
    nbrPost,nbrPre = np.shape(weights)
    weights = np.reshape(weights,(nbrPost*nbrPre))
    plt.figure()
    plt.hist(weights,50)
    plt.savefig('weightHistV1toIN.png')
    

def createFields(directory):
    createDir()
    files = listdir(directory)
    for data in files:
        w = loadData(directory+'/'+data)
        fields = reshapeFields(w)
        plotONOFF(fields,data)
    plotWeightHist(files)
        
def main():    
    createFields('exitatory')

    print('finish')
if __name__ == "__main__":
    main()

## @package cwfs
## @file validation.py
## @brief validation script for cwfs
##
## @authors: Bo Xin & Chuck Claver
## @       Large Synoptic Survey Telescope

import os
import numpy as np
import matplotlib.pyplot as plt

from cwfsInstru import cwfsInstru
from cwfsAlgo import cwfsAlgo
from donutImage import donutImage
from cwfsAlgo import getZer4Up

imgDir=['../testImages/F1.23_1mm_v61',
        '../testImages/LSST_C_SN26', '../testImages/LSST_C_SN26',
        '../testImages/LSST_NE_SN25','../testImages/LSST_NE_SN25']
intra=['z7_0.25_intra.txt',
        'z7_0.25_intra.txt', 'z7_0.25_intra.txt',
        'z11_0.25_intra.txt', 'z11_0.25_intra.txt']
extra=['z7_0.25_extra.txt',
        'z7_0.25_extra.txt', 'z7_0.25_extra.txt',
        'z11_0.25_extra.txt', 'z11_0.25_extra.txt']
fldxy=np.array([[0,0],[0,0],[0,0],[1.185,1.185],[1.185,1.185]])
myalgo=['fft','fft','exp','fft','exp']
mymodel=['paraxial','onAxis','onAxis','offAxis','offAxis']
myinst='lsst'

validationDir='validation'
matlabZFile=['F1.23_1mm_v61_z7_0.25_fft.txt',
             'LSST_C_SN26_z7_0.25_fft.txt','LSST_C_SN26_z7_0.25_exp.txt',
             'LSST_NE_SN25_z11_0.25_fft.txt','LSST_NE_SN25_z11_0.25_exp.txt']

znmax=22
nTest=len(intra)
zer=np.zeros((znmax-3,nTest))
matZ=np.zeros((znmax-3,nTest))
x=range(4,znmax+1)

fig = plt.figure(figsize=(10, 10))

for j in range(nTest):
    intraFile=os.path.join(imgDir[j],intra[j])
    extraFile=os.path.join(imgDir[j],extra[j])
    I1=donutImage(intraFile,fldxy[j,:],'intra')
    I2=donutImage(extraFile,fldxy[j,:],'extra')

    inst=cwfsInstru(myinst,I1.sizeinPix)
    algo=cwfsAlgo(myalgo[j],inst,1)
    algo.runIt(inst,I1,I2,mymodel[j])
    zer[:,j]=getZer4Up(algo,'nm')

    matZ[:,j]=np.loadtxt(os.path.join(validationDir,matlabZFile[j]))

    ax = plt.subplot(nTest, 1, j)
    plt.plot(x,matZ[:,j],label='Matlab',marker='o',color='r',markersize=10)
    plt.plot(x, zer[:,j],label='Python',marker='.',color='b',markersize=10)
    plt.legend(loc="upper right", shadow=True, title=matlabZFile[j], fancybox=True)
    ax.get_legend().get_title().set_color("red")

plt.show()

    
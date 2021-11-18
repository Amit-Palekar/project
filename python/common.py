import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage
from matplotlib import gridspec
import math

# the function to find index from the oversampled space for the sampled time point
def findIdx(v_s, v_vector):
    v_diff = abs( v_vector - v_s)
    resultA = np.where( v_diff == np.amin(v_diff) );
    idx = int( resultA[0])
    return idx

# a function to edit plots in the script
def editfPlot(Ft,Fx,ft,fx,dispRange,xlabeltxt, ylabeltxt, titletxt):
    # Ft: temporal dimension range
    # Fx: spatial dimension range
    # ft: temporal axis vector
    # fx: spatial axis vector
    # dispRange: display range of the x and y axis
    idxt = [findIdx(dispRange[0], ft), findIdx(dispRange[1], ft)]
    idxx = [findIdx(dispRange[2], fx), findIdx(dispRange[3], fx)]   
    tticksP = np.array( [idxt[0], len(ft)/2, idxt[1]] )
    xticksP = np.array( [idxx[0], len(fx)/2, idxx[1]] );
    tticksL = (Ft*(tticksP - len(ft)/2)/len(ft)).tolist()
    xticksL = (Fx*(xticksP - len(fx)/2)/len(fx)).tolist()
    ttickslabels = [str(tticksL[0]), str(tticksL[1]), str(tticksL[2]) ];
    xtickslabels = [str(xticksL[0]), str(xticksL[1]), str(xticksL[2]) ];
    plt.xlim( [idxt[0], idxt[1]] )
    plt.ylim( [idxx[0], idxx[1]] )
    plt.xticks( tticksP, ttickslabels,fontsize = 16)
    plt.yticks( xticksP, xtickslabels,fontsize = 16)
    plt.gca().set_aspect((idxt[1] - idxt[0])/(idxx[1] - idxx[0]))
    plt.xlabel(xlabeltxt,fontsize = 18)
    plt.ylabel(ylabeltxt,fontsize = 18)
    plt.title(titletxt, fontsize = 20)
    return
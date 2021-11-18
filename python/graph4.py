import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage
from matplotlib import gridspec
import math
from common import *
from graph3 import *
from io import BytesIO
import base64
import sys

# calculate the frequency spectrum of the continous signal
fresult_c = np.fft.fftshift(np.fft.fft2(l_xt))
f_amp_c = abs(fresult_c)/((len(x) * len(t)))
# calculate the frequency spectrum of the sampled signal
#( we can later apply a Hanning window to remove the effect of limited signal length, i.e. a sinc-shaped envolope)
fresult = np.fft.fftshift(np.fft.fft2(l_xts))
f_amp = abs(fresult)/(len(x) * len(t))
Ft = len(t)/recordingLength
Fx = len(x)/visualRange
ft = Ft*( np.arange(0, len(t),1) - len(t)/2) / len(t)
fx = Fx*( np.arange(0, len(x),1) - len(x)/2) / len(x)

# print(np.max(ft))
# print(np.max(fx))

xlabel_txtf = 'Temporal Frequency (Hz)'
ylabel_txtf = 'Frequency (cycles/degree)'
dispRangeF =  [-600, 600, -200, 200]

def run():
    fig2 = plt.figure(figsize= (20, 20))
    nrows = 1 
    ncols = 2
    gs = gridspec.GridSpec(nrows, ncols,figure=fig2)
    fig2.add_subplot(gs[0, 0]) 
    plt.imshow(f_amp_c, vmin=np.amin(f_amp_c), vmax=0.5*np.amax(f_amp_c))
    editfPlot(Ft,Fx,ft,fx, dispRangeF,xlabel_txtf,ylabel_txtf, 'Continous Signal frequency spectrum')

    fig2.add_subplot(gs[0, 1])
    plt.imshow(f_amp, vmin=np.amin(f_amp), vmax=0.5*np.amax(f_amp))
    editfPlot(Ft,Fx,ft,fx, dispRangeF,xlabel_txtf,ylabel_txtf, 'Sampled Signal frequency spectrum')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    print(base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', ''))
    buf.close()

if __name__ == '__main__':
    run()

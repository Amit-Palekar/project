# Now define the contast sensitivity function of the human visual system 
# for now, consider temporal CSF and spatial CSF as separate. 
# add spatial CSF. temporal CSF remains to be added

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage
from matplotlib import gridspec
import math
from common import *
from graph3 import *
from graph4 import *
from io import BytesIO
import base64
import sys

L = float(sys.argv[14]) # luminance of stimulus
wl = float(sys.argv[15]) # Hz
ul = float(sys.argv[16]) # cycles/degree
##--------------------------------------- end of use input

[ww, uu] = np.meshgrid(ft,fx)
rect = False
if rect: 
    filter_eye = np.multiply ( np.logical_and( abs(ww) < wl, abs(uu) < ul ) , 1)
else: 
    # model of CSF (over spatial frequency): 
    Su = 5200*np.exp(-0.0016*((1+100/L)**0.08)*uu**2 )\
    /np.sqrt( (1+144/(objSizeNpxl*pxlSize)**2 + 0.64*uu**2)*(63/L**0.83 + 1/(1-np.exp(-0.002*uu**2))) )
    # # # # empirical function of CSF (over spatial frequency):
    # # Su = 540*(1+0.7/L)**(-0.2)/(1 + 12/(objSizeNpxl*pxlSize*(1+abs(uu)/3)))*abs(uu)*np.exp(-0.3*(1+100/L)**0.15*abs(uu))\
    # # *np.sqrt(1+0.06*np.exp(0.3*(1+100/L)**0.15*abs(uu)))
    filter_eye = np.multiply(abs(ww)<wl, Su)

fig4 = plt.figure(figsize=(20,20))
f_filtered_c = np.multiply(fresult_c, filter_eye)
f_filtered = np.multiply(fresult, filter_eye)

def run():
	nrows = 2
	ncols = 2
	gs = gridspec.GridSpec(nrows, ncols,figure=fig4)
	# fig3 = plt.figure(figsize= (7,7))
	fig4.add_subplot(gs[0, 0])
	plt.imshow(filter_eye)
	editfPlot(Ft,Fx,ft,fx,dispRangeF,xlabel_txtf, ylabel_txtf,'Window of visibility')
	# now apply the filtering effect of the eye
	
	fig4.add_subplot(gs[1, 0])
	plt.imshow(abs(f_filtered_c), vmin=np.amin(abs(f_filtered_c)), vmax=0.2*np.amax(abs(f_filtered_c)))
	editfPlot(Ft,Fx,ft,fx,dispRangeF,xlabel_txtf, ylabel_txtf, 'Continous signal filtered spectrum')
	fig4.add_subplot(gs[1, 1])
	plt.imshow(abs(f_filtered), vmin=np.amin(abs(f_filtered)), vmax=0.2*np.amax(abs(f_filtered)))
	editfPlot(Ft,Fx,ft,fx,dispRangeF,xlabel_txtf, ylabel_txtf, 'Sampled signal filtered spectrum')

	buf = BytesIO()
	plt.savefig(buf, format='png', bbox_inches='tight')
	plt.close()
	print(base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', ''))
	buf.close()

if __name__ == '__main__':
    run()



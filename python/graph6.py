import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage
from matplotlib import gridspec
import math
from common import *
from graph3 import *
from graph4 import *
from graph5 import *
from io import BytesIO
import base64
import sys

def run():
	# now perform Inversve Fourier Transform and predict what our eyes will see
	f_recon_c = abs(np.fft.ifft2(np.fft.fftshift(f_filtered_c)) )
	f_recon = abs( np.fft.ifft2(np.fft.fftshift(f_filtered)))
	fig5 = plt.figure(figsize= (20,20))
	xlabel_txtt = 'Time (s)'
	ylabel_txts = 'Space (degree)'
	dispRangets = [0, recordingLength, 0, recordingLength*v]
	nrows = 1
	ncols = 2
	gs = gridspec.GridSpec(nrows, ncols,figure=fig4)
	fig5.add_subplot(gs[0, 0])
	plt.imshow(f_recon_c, vmin = np.amin(f_recon_c), vmax= 0.8*np.amax(f_recon_c))
	editfPlot(recordingLength,visualRange,t,x,dispRangets, xlabel_txtt, ylabel_txts, 'Reconstruction of continous signal')
	fig5.add_subplot(gs[0, 1])
	plt.imshow(f_recon, vmin = np.amin(f_recon), vmax= 0.8*np.amax(f_recon))
	editfPlot(recordingLength,visualRange,t,x,dispRangets, xlabel_txtt, ylabel_txts, 'Reconstruction of sampled signal')

	buf = BytesIO()
	plt.savefig(buf, format='png', bbox_inches='tight')
	plt.close()
	print(base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', ''))
	buf.close()

if __name__ == '__main__':
    run()
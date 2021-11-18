import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import scipy.ndimage as ndimage
from matplotlib import gridspec
import math
from common import *
# from graph1 import *
from io import BytesIO
import base64
import sys

# configure the continuous/oversampled stimulus
# configure the original (i.e. over sampled) stimulus
# velocity along x and y axis for a line infinitely long in z (i.e. the direction perpendicular to the screen)
# note size of the stimulus is not considered here. Size of the stimulus will be taken in to account in the ...
# part to configure the sampled signal. 
vx = float(sys.argv[1]) # degrees/s
vy = float(sys.argv[2]) # degrees/s
x0 = float(sys.argv[3])
y0 = float(sys.argv[4])
# create the x-y-t space;
recordingLength = float(sys.argv[5]) # seconds
t_interval = float(sys.argv[6]) # sec
xy_interval = min(vx*t_interval,0.0002) # degree
objSize = float(sys.argv[7]) # size of the object, in degrees
## ---------------end of user input


# for 2D motion, take advantage of the rotation properties of Fourier Transform
v = math.sqrt(vx**2 + vy**2) # the amplitude of velocity
# the angle of the velocity; i.e. the orientation of the motion axis
if vx == 0:
    axisRotate = 90
    x_interval = xy_interval
elif vy == 0:
    axisRotate = 0
    x_interval = xy_interval
else: 
    axisRotate = 180* (np.arctan(vy/vx))/math.pi 
    x_interval = xy_interval*math.sqrt(1 + (min(vy/vx, vx/vy))**2 )
# print('Axis orientation: ', axisRotate, '  space interval: ', x_interval, 'cycles/degree;  time interval: ', t_interval, 's')
visualRange = v*recordingLength
t = np.arange(0, recordingLength, t_interval) # time range
x = np.arange(0, visualRange, x_interval) # space range (in degrees)
l_xt = np.zeros([len(x), len(t)])

# the following commands use too much memory, since tt and xx are both large
# [tt,xx] = np.meshgrid(t,x)
# contrast distribution function
# l_line =abs( xx - vx*tt - x0 )
# l_xt = (np.multiply( l_line < x_interval , 1)).astype('int') # delta function: 1 at 0, 0 at all other spaces.


for i in range(0, len(t)):
    xi = v*t[i]
    t_idx = findIdx(t[i], t)
    x_idx = findIdx(xi, x)  
    l_xt[x_idx:x_idx+ round(objSize/x_interval),t_idx] = 1   

# create the sampled version of the signal
captureRate = float(sys.argv[8]) # Hz 
holdingFactor = float(sys.argv[9]) # pixel holding factor, range of 0-1 (e.g. if same value is held until next sample point, then holding factor equals to 1)
pxlSize = float(sys.argv[10]) # unit: degrees; this is the pixel size of a 3840 pixel display with an angle FOV of 30 degrees. 
# objSize = float(0)
# recordingLength = float(0.078)
objSizeNpxl = math.ceil(objSize/pxlSize)# size of the object, in number of pixels
# print(objSizeNpxl)
fillF = float(sys.argv[11]) # pixel fill factor, range of 0-1
antialiasing = sys.argv[12] == 'true' # if use Gaussian antialiasing
antialiasingF = float(sys.argv[13]) # ignored if antialiasing is False
## ----------- end of user input

t_s = (np.arange(0, captureRate*recordingLength,1))/captureRate # samples' time stamps
tt_idx =  (np.zeros([len(t_s)])).astype(int)  # index of the time stamps sampled points
l_xts = np.zeros(l_xt.shape) # sampled signal space
xx_idx = (np.zeros(tt_idx.shape)).astype(int) # index of the position vector of sampled points
smp1D = np.zeros(x.shape) # line image at a single time point
pxl1D = np.zeros( round(len(x)/(pxlSize/x_interval)) )# line image equals to the number of pixels (each pixel contains pxlSize/x_interval sub pixels )

for i in range(len(t_s)): 
    tt_idx[i] = findIdx(t_s[i], t) # find the matched time stamp in the orignial signal
    smp1D[:] = 0 # initialize smp 1D
    pxl1D[:] = 0 # intialize pxl1D
    #     plt.figure()
    #     plt.plot( l_xt[:,tt_idx[i]])
    #     print(pxl1D)
    if i < len(t_s)-1: # the last sample point will not have an updated sample interval 
        tt_idxNext = findIdx(t_s[i+1],t)
        smpInterval = tt_idxNext - tt_idx[i]  
    
    xx_idx[i] = findIdx(vx*t[tt_idx[i]], x)
    pxlVidx = math.floor(xx_idx[i]/(pxlSize/x_interval))
    pxl1D[pxlVidx: min(len(pxl1D),pxlVidx + objSizeNpxl)] = l_xt[xx_idx[i],tt_idx[i]]
    if antialiasing:
        pxl1D = ndimage.gaussian_filter1d(pxl1D,antialiasingF)
    # print(pxl1D)
    # now fill in the values based on pixel fill factor. 
    for j in range(len(pxl1D)):
        smp1D[j*round(pxlSize/x_interval): \
              j*round(pxlSize/x_interval) + math.ceil(math.sqrt(fillF)*pxlSize/x_interval)] = pxl1D[j]
              
    l_xts[:,tt_idx[i]] = smp1D
    #     fig = plt.figure()   
    #     plt.xlim([0, 3000])
    #     plt.plot(smp1D)
    # Now fill in the values decided by temporal holding factor. 
    # the range of sample and hold (staircase function)
    stairCaseRange= np.arange(tt_idx[i],min(tt_idx[i] + round( holdingFactor*smpInterval ), len(t)-1),1)
    for j in range( len(stairCaseRange) ):
        l_xts[:, int(stairCaseRange[j])] = l_xts[:, int(stairCaseRange[0])]  
    
def run():
    fig1 = plt.figure(figsize= (20, 20))
    xlabel_txtt = 'Time (s)'
    ylabel_txts = 'Space (degree)'
    dispRangets = [0, recordingLength, 0, recordingLength*v]
    nrows = 1 
    ncols = 2
    gs = gridspec.GridSpec(nrows, ncols,figure=fig1)
    fig1.add_subplot(gs[0, 0]) 
    plt.imshow(l_xt, vmin = 0, vmax = 0.2)
    editfPlot(recordingLength, visualRange, t, x, dispRangets, xlabel_txtt, ylabel_txts, 'Continous Signal')

    fig1.add_subplot(gs[0, 1])
    plt.imshow(l_xts, vmin = 0, vmax = 0.2)
    editfPlot(recordingLength, visualRange, t, x, dispRangets, xlabel_txtt, ylabel_txts, 'Sampled Signal')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    print(base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', ''))
    buf.close()

if __name__ == '__main__':
    run()


import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
from matplotlib import gridspec
from io import BytesIO
import base64
import sys

# configure the stimulus
# configure the original (i.e. over sampled) stimulus
# velocity along x and y axis for a line infinitely long in z (i.e. the direction perpendicular to the screen)
vx = 2 # degrees/s
vy = 1 # degrees/s
x0 = 0
y0 = 0
recordingLength = 10 # seconds
# create the x-y-t space;
t_interval = 0.005 # sec
x_interval = 0.005 # degree
angleRange= 30 # degree

t = np.arange(0, recordingLength, t_interval) # time range
x = np.arange(0, angleRange, x_interval) # space range (in degrees)
[tt,xx] = np.meshgrid(t,x)
# contrast distribution function
l_line =abs( xx - vx*tt - x0 )
l_xt = (np.multiply( l_line < x_interval , 1)).astype('int') # delta function: 1 at 0, 0 at all other spaces. 

# create the sampled version of the signal
samplingRate = 100 # Hz 
sampleAndHold = True # if sample and hold (i.e. staircase) or not
t_s = (np.arange(0, samplingRate*recordingLength,1))/samplingRate # samples' time stamps
tt_idx =  (np.zeros([len(t_s)])).astype(int)  # index of the time stamps sampled points
l_xts = (np.zeros(l_xt.shape)).astype(int) # sampled signal space
xx_idx = (np.zeros(tt_idx.shape)).astype(int) # index of the position vector of sampled points
for i in range(len(t_s)): 
    tt_diff = abs(t - t_s[i])
    resultt = np.where( tt_diff == np.amin(tt_diff) )
    tt_idx[i] = int( resultt[0]) # find the matched time stamp in the orignial signal
    xx_diff = abs(x - vx*t[tt_idx[i]])
#     print(tt_idx[i],t_s[i],t[tt_idx[i]])
    resultx = np.where( xx_diff == np.amin(xx_diff) );
    xx_idx[i] = int( resultx[0])
#     print(tt_idx[i],t_s[i],t[tt_idx[i]], x[xx_idx[i]])
    l_xts[xx_idx[i], tt_idx[i]] = l_xt[xx_idx[i], tt_idx[i]] # extract the contrast from the original signal

if sampleAndHold: # if under sample and hold mode, points in between the two samples will be set as the first sample
    for i in range(len(t_s)-1) :
        stairCaseRange= np.arange(tt_idx[i],tt_idx[i + 1],1) # the index range of the staircase function
        l_xts[xx_idx[i], stairCaseRange] = l_xt[xx_idx[i], tt_idx[i]]
#         print(stairCaseRange)   
fig = plt.figure(figsize= (200, 200))
# nrows = 1 
# ncols = 2
# gs = gridspec.GridSpec(nrows, ncols,figure=fig)
# ax = fig.add_subplot(gs[0, 0]) 
plt.imshow(l_xts)
# ax2 = fig.add_subplot(gs[0, 1])
# plt.imshow(l_xts[0:int(1/x_interval/5) ][0:int(1/t_interval/5)],cmap = 'gray')

buf = BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight')
plt.close()
print(base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', ''))
buf.close()
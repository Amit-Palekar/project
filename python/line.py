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
vx = float(sys.argv[1]) # degrees/s
vy = float(sys.argv[2]) # degrees/s
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
plt.figure(figsize=(40,20))
plt.imshow(l_xt, cmap = 'gray')

buf = BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight')
plt.close()
print(base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', ''))
buf.close()
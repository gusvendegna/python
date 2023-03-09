import numpy as np
import matplotlib.pyplot as plt
from math import *

import numpy.random as rng
rng.seed(1001)

T = 10                     # [s]  total time
F = 0.01                   # [Hz] sampling rate

nt = int(T/F)              # samples
f  = 0.5                   # signal frequency
k  = 0.2                   # signal damping 

t = np.linspace(0,10,nt)   # time axis

s = np.sin(2*pi*f*t) * np.exp(-k*t)

# start with the signal
a = s.copy()

# add white noise
wn = rng.uniform(-0.2,+0.2, nt)
a += wn

# add spiky noise
ns = 51
sn = np.zeros(nt)
sn[ rng.randint(1,nt,ns) ] = rng.uniform(-5.0,+5.0,ns)
a += sn

plt.figure(figsize=(15,5))

plt.plot(t,a,'k')
plt.xlabel('t') 
plt.ylabel('a') 
plt.ylim(-5.1,+5.1);

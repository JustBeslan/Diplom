import matplotlib.pyplot as plt 
from scipy.fftpack import fft 
from scipy.io import wavfile # get the api 
import math
import cmath
import numpy as np

fs, data = wavfile.read('/home/beslan/woman1.wav') # load the data 
a = data.T[0] # this is a two channel soundtrack, I get the first track 
b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1) 

c = fft(b) # calculate fourier transform (complex numbers list)
d = len(c)/2 # you only need half of the fft list (real signal symmetry) 
plt.plot(abs(c[0:600]),'r') 

b = [amp * 1.8 * (0.5 - 0.5 * math.cos(2*np.pi*i/len(b))) for i, amp in enumerate(b)]
c = fft(b) # calculate fourier transform (complex numbers list)
d = len(c)/2 # you only need half of the fft list (real signal symmetry) 
#plt.plot(abs(c[0:600]),'g')

c = [cmath.log(amp) for i, amp in enumerate(list(c))]
c2 = fft(c)
d2 = len(c2)/2 # you only need half of the fft list (real signal symmetry) 
#plt.plot(abs(c2[0:600]),'b')

fund_freq = len(c2) / (np.argmax(c2[178:600]) + 30.0)
print(48000 * fund_freq / len(c2))

plt.show() 

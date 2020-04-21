import matplotlib.pyplot as plt 
from scipy.fftpack import fft 
from scipy.io import wavfile # get the api 
import math
import cmath
import numpy as np

fs, data = wavfile.read('/home/beslan/woman1.wav') # load the data 
a = data.T[0] # this is a two channel soundtrack, I get the first track 
print(len(a))
ch = 100
size1 = len(a)
while ((size1%(ch//2)) != 0): 
	size1 = size1 - 1
print(size1)
x = np.zeros((size1,ch))
print(size1)
for i in range(size1//(ch//2)-1):
	x[i] = a[int(ch*(i/2)):int(ch*(i/2+1))]
	b=[(ele/2**8.)*2-1 for ele in x[i]] # this is 8-bit track, b is now normalized on [-1,1) 

	c = fft(b) # calculate fourier transform (complex numbers list)
	d = len(c)/2 # you only need half of the fft list (real signal symmetry) 
	plt.plot(abs(c[:int(d-1)]),'r') 

plt.show()

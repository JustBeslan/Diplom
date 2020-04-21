from struct import *
import matplotlib.pyplot as plt
import numpy as np

def read_file(filename):
	f = open(filename, "rb")
	chunk = f.read(2)
	raw_input1 = []
	while chunk:
		raw_input1.append(unpack('<h', chunk)[0])
		chunk = f.read(2)
	f.close()
	return raw_input1

def dft(fnList):
	fnList = np.asarray(fnList,dtype=float)
	N = fnList.shape[0]
	n = np.arange(N)
	FmList = []
	for m in range(N):
		Fm = 0.0
		for n in range(N): Fm += fnList[n] * cmath.exp(- 2j * np.pi * m * n / N)
		FmList.append(abs(Fm / N))
	return FmList

raw_input = read_file("/home/beslan/a3_2.wav")
spectrum = dft(raw_input)
plt.plot(spectrum[0:400], 'r')
plt.show()
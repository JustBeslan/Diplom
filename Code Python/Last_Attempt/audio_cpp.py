import soundfile as sf
import matplotlib.pyplot as plt
from numpy.fft import rfft, rfftfreq
from numpy import array, arange, abs as np_abs

data, fs = sf.read('/home/beslan/a2.wav')
spectrum = rfft(data)

N = len(data)
FD = 22050

plt.plot(rfftfreq(N, 1./FD), np_abs(spectrum)/N)
plt.grid(True)
plt.show()

print("%3d" % data)
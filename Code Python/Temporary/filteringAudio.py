import numpy as np
import math
from scipy.signal import butter, lfilter
from scipy.io import wavfile

path = "/home/beslan/Diplom/WorkWithVideo4/Audio/"
name = "Audiotest2.wav"

fs_rate, signal = wavfile.read(path + name)
signal = np.array(signal)

signal_1 = signal[:,0]
signal_2 = signal[:,1]
slice_ms = 1000

h = int((fs_rate/1000) * slice_ms)				# Always value parameter slice_ms should be >= 10
count_h = math.ceil(len(signal_1) / h)			# This is so time video(h = fs_rate).
print(count_h)
#=========Готовим постоянные данные для фильтрации каждой части аудио============
lowcut = 300
highcut = 3000
nyq = 0.5 * fs_rate
low = lowcut / nyq
high = highcut / nyq
b, a = butter(6, [low, high], btype='band')
#================================================================================
Filtered = signal.copy()

for i in range(0,count_h):
	Filtered[:,0][i*h:(i+1)*h] = lfilter(b, a, signal_1[i*h:(i+1)*h])
	Filtered[:,1][i*h:(i+1)*h] = lfilter(b, a, signal_2[i*h:(i+1)*h])

wavfile.write(path + "Filtered_" + name, fs_rate, Filtered)
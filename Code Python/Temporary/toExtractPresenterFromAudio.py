import matplotlib.pyplot as plt
import librosa
import librosa.display
import sklearn
import numpy as np
import scipy
import math

path = '/home/beslan/Diplom/WorkWithVideo5/Audio/'
name = 'Audiotest3.wav'

def confidence(x, y):
	return np.sum((x - y)**2) # Евклидово расстояние
	# Меньше — лучше

x, sr = librosa.load(path + name)
slice_ms = 125

h = int((sr/1000)*slice_ms)
count_h = math.ceil(len(x) / h)

afss_norm = []
x1 = []

for i in range(0,count_h):
	x1.append(x[i*h:(i+1)*h])

for i in range(0,len(x1)):
	afs = librosa.feature.mfcc(x1[i],sr=sr,n_mfcc=32, n_fft=2048)
	afss = np.sum(afs[2:], axis=-1)
	afss_abs = np.abs(afss)
	afss_max = np.max(afss_abs)
	if (afss_max != 0):
		afss = afss/afss_max
		afss_norm.append(afss)

indexes = []
dist = np.array([])

print(len(afss_norm))

for i in range(0,len(afss_norm)):
	indexes.append([])
	for j in range(i,len(afss_norm)):
		indexes.append([i,j])
		dist = np.append(dist,confidence(afss_norm[i],afss_norm[j]))

print(dist)
max_dist = np.max(np.abs(dist))
dist = dist / max_dist

indexes = []
for i in range(0,len(dist)):
	if (dist[i] <= 0.5):
		indexes.remove(indexes[i])


# max_len = np.max([len(e) for e in dist])
# print(len(x1))
# indexes = list(filter(lambda e: len(e) == max_len,dist))[0]
indexes = list(set(indexes))
# print(len(indexes))

part_data = []
for i in indexes:
	part_data.extend(x1[i])

librosa.output.write_wav(path + 'Others.wav',np.array(part_data),sr)









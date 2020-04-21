import os
import math
import wave
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from moviepy.editor import *
from pydub import AudioSegment


def to_extractAudioFromVideo(pathDir):
	files = os.listdir(pathDir)
	videoclip = VideoFileClip(pathDir + "/" + files[0])
	audioclip = videoclip.audio
	dirWithAudio = pathDir + "/Audio"
	os.makedirs(dirWithAudio)
	audioclip.write_audiofile(dirWithAudio + "/Audio" + os.path.splitext(files[0])[0] + ".wav")

	return dirWithAudio + "/"

def distanceBetweenMatrix(Matrix1, Matrix2):
	# все матрицы 20x44
	differenceMatrixes = np.array(Matrix1) - np.array(Matrix2)
	SquareDifferenceMatrixes = differenceMatrixes**2
	return np.sum(SquareDifferenceMatrixes)**0.5

def audioAnalyze(path, name, slice_ms=100):
	fs_rate, signal = wavfile.read(path + name)
	signal = np.array(signal)

	signal_1 = signal[:,0]
	signal_2 = signal[:,1]

	# signal = signal.mean(axis=1)
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
	Silence = np.zeros(2*len(signal),dtype="int16").reshape(len(signal),2)
	Voices = np.zeros(2*len(signal),dtype="int16").reshape(len(signal),2)
	j = 0
	k = 0
	for i in range(0,count_h):
		partData_1 = signal_1[i*h:(i+1)*h]
		filtered_data_1 = lfilter(b, a, partData_1)
		Filtered[:,0][i*h:(i+1)*h] = filtered_data_1

		partData_2 = signal_2[i*h:(i+1)*h]
		filtered_data_2 = lfilter(b, a, partData_2)
		Filtered[:,1][i*h:(i+1)*h] = filtered_data_2

		countElementsOfBreakingTheSilence_1 = len(list(filter(lambda e: e>=10.6 or e<=-10.6,filtered_data_1)))
		countElementsOfBreakingTheSilence_2 = len(list(filter(lambda e: e>=10.6 or e<=-10.6,filtered_data_2)))

		if (countElementsOfBreakingTheSilence_1 >= 100 and countElementsOfBreakingTheSilence_2 >= 100):
			# mfcc_characterisits.append([intervalTime_str,librosa.feature.mfcc(filtered_data,sr=fs_rate),True])
			# partsData_SomeoneSays.append(partData_2)
			Voices[:,0][k*h:(k+1)*h] = filtered_data_1
			Voices[:,1][k*h:(k+1)*h] = filtered_data_2
			Silence = Silence[:len(Silence)-len(filtered_data_1)]
			k += 1
		else:
			Voices = Voices[:len(Voices)-len(filtered_data_1)]
			Silence[:,0][j*h:(j+1)*h] = filtered_data_1
			Silence[:,1][j*h:(j+1)*h] = filtered_data_2
			j += 1
		if (i%10000 == 0):
			print(i)

	# plt.figure(1)
	# plt.plot(np.linspace(0,len(Voices)/fs_rate,num=len(Voices)),Voices)
	# plt.show()

	wavfile.write(path + "Filtered_" + name, fs_rate, Filtered)
	wavfile.write(path + "Silence_" + name, fs_rate, Silence)
	wavfile.write(path + "Voices_" + name, fs_rate, Voices)
	
	print("AAAA2")

	print(len(mfcc_characterisits))

	for i in range(0,len(mfcc_characterisits)):
		if (mfcc_characterisits[i][2]):
			mfcc_characterisits[i][2] = False
			distances.append([i])
			q = []
			for j in range(i,len(mfcc_characterisits)):
				if (mfcc_characterisits[j][2]):
					q.append(distanceBetweenMatrix(mfcc_characterisits[i][1],mfcc_characterisits[j][1]))
			if (q != []):
				qmax = np.max(q)
				q1 = [e/qmax for e in q]
				for k in range(i,len(q1)):
					if (q1[k] <= 0.6):
						mfcc_characterisits[k][2] = False
						distances[len(distances)-1].append(k)
			# for j in range(i,len(mfcc_characterisits)):
			# 	dist = distanceBetweenMatrix(mfcc_characterisits[i][1],mfcc_characterisits[j][1])
			# 	q.append(dist)
			# 	if (mfcc_characterisits[j][2] and  dist<= 150):
			# 		mfcc_characterisits[j][2] = False
			# 		distances[len(distances)-1].append(j)
		if (i%1000 == 0):
			print("i = ",i,"q1 = ",q1)

	# max_len = np.max([len(d) for d in distances])
#	print(max_len)
	# max_enviroment = list(filter(lambda e: len(e) == max_len,distances))[0]
#	print(max_enviroment)
	# partsData_SaysMain = np.ravel([partsData_SomeoneSays[i] for i in max_enviroment])
	# wavfile.write(path + "Main_" + name, fs_rate, partsData_SaysMain)

	# partsData_NobodySaid2 = np.array(partsData_NobodySaid2, dtype="float32")
	# print(partsData_NobodySaid2)
	# partsData_NobodySaid2 = np.ravel(partsData_NobodySaid2)
	# wavfile.write(path + "Silence_" + name, fs_rate, partsData_NobodySaid2)
	# print(len(partsData_NobodySaid2))

def to_extractPresenterFromAudio(path, name, slice_ms=500):
	fs_rate, signal = wavfile.read(path + name)
	signal = np.array(signal)

	signal_1 = signal[:,0]
	signal_2 = signal[:,1]

	# signal = signal.mean(axis=1)
	h = int((fs_rate/1000) * slice_ms)				# Always value parameter slice_ms should be >= 10
	count_h = math.ceil(len(signal_1) / h)			# This is so time video(h = fs_rate).
	print(count_h)

	mfcc_characterisits_1 = []
	mfcc_characterisits_2 = []

	print("mfcc")
	for i in range(0,count_h):
		partData_1 = signal_1[i*h:(i+1)*h]
		partData_2 = signal_2[i*h:(i+1)*h]

		mfcc_characterisits_1.append([librosa.feature.mfcc(np.array(partData_1,dtype='float32'),sr=fs_rate),True])
		mfcc_characterisits_2.append([librosa.feature.mfcc(np.array(partData_2,dtype='float32'),sr=fs_rate),True])

		if (i%1000 == 0):
			print(i)

	distances_1 = []
	distances_2 = []
	print(len(mfcc_characterisits_1))

	print("distances")
	for i in range(0,len(mfcc_characterisits_1)):
		if (mfcc_characterisits_1[i][1] and mfcc_characterisits_2[i][1]):
			for j in range(i,len(mfcc_characterisits_1)):
				if (mfcc_characterisits_1[j][1] and mfcc_characterisits_2[j][1]):
					if (mfcc_characterisits_1[j][0].shape[1] == mfcc_characterisits_1[i][0].shape[1]):
						distance_1 = distanceBetweenMatrix(mfcc_characterisits_1[i][0],mfcc_characterisits_1[j][0])
						distance_2 = distanceBetweenMatrix(mfcc_characterisits_2[i][0],mfcc_characterisits_2[j][0])
						distances_1.append([i,j,distance_1])
						distances_2.append([i,j,distance_2])
						mfcc_characterisits_1[j][1] = False
						mfcc_characterisits_2[j][1] = False
		if (i%1000 == 0):
			print(i)

	# max_len_1 = np.max([d for i,j,d in distances_1])
	# max_len_2 = np.max([d for i,j,d in distances_2])
	# distances_1 = [[i,j,d/max_len_1] for i,j,d in distances_1]
	# distances_2 = [[i,j,d/max_len_2] for i,j,d in distances_2]
	distances = []
	for i in range(0,len(distances_1)):
		if (distances_1[i][2] <= 3350 and distances_2[i][2] <= 3350):
			distances.append(distances_1[i][0])
			distances.append(distances_1[i][1])

	distances = [e for e in set(distances)]

	print("file")
	partsData_SaysMain = np.zeros(2*len(distances)*h,dtype="int16").reshape(len(distances)*h,2)
	for i in range(0,len(distances)):
		l = len(signal_1[distances[i]*h:(distances[i]+1)*h])
		if (l == h):
			partsData_SaysMain[:,0][i*h:(i+1)*h] = signal_1[distances[i]*h:(distances[i]+1)*h]
			partsData_SaysMain[:,1][i*h:(i+1)*h] = signal_2[distances[i]*h:(distances[i]+1)*h]
		else:
			partsData_SaysMain[:,0][i*h:i*h+l] = signal_1[distances[i]*h:(distances[i]+1)*h]
			partsData_SaysMain[:,1][i*h:i*h+l] = signal_2[distances[i]*h:(distances[i]+1)*h]			

	print("len = ",len(partsData_SaysMain[0]))
	wavfile.write(path + "Main_" + str(i), fs_rate,partsData_SaysMain)
		# else:
		# 	othersParts = [[],[]]
		# 	for index in indexes:
		# 		othersParts[:,0].append(signal_1[index*h:(index+1)*h])
		# 		othersParts[:,1].append(signal_2[index*h:(index+1)*h])

		# 	wavfile.write(path + "Other_" + i, fs_rate,othersParts)



"""
def audioFilterNoiseButterFilter(path, name, lowcut=300, highcut=3000):
    sound_track = wave.open(path + name, 'r')

    nframes = sound_track.getnframes()
    framerate = sound_track.getframerate()
    T = nframes / framerate

    t = np.linspace(0, T, nframes, endpoint=False)
    sound_track.close()

    fs, data = wavfile.read(path + name)
    new_data = []

    for i in range(len(data)):
        new_data.append(data[i][0])

    new_data = np.array(new_data, dtype="float32")

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(6, [low, high], btype='band')

    filtered_data = lfilter(b, a, new_data)

    filtered_data = np.array(filtered_data, dtype="int16")
    wavfile.write(path + "Filtered_" + name, fs, filtered_data)
"""

# dirWithAllAudio = to_extractAudioFromVideo("/home/beslan/Diplom/WorkWithVideo4")
# audioAnalyze("/home/beslan/Diplom/WorkWithVideo4/Audio/","Audiotest2.wav")
to_extractPresenterFromAudio("/home/beslan/Diplom/WorkWithVideo4/Audio/","Filtered_Audiotest2.wav")
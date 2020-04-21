import librosa
import numpy as np
import math
import matplotlib.pyplot as plt

# window_ms = 1000
# margin_ms = window_ms//2

# path = '/home/beslan/Diplom/Test5/Audio/data/chunks/'
# name = 'chunk-002.wav'
path = '/home/beslan/Diplom/Test3/Audio/'
name = 'VoicesAudiotest3.wav'

low = 300
high = 8000
countFilters = 26
countCoeffic = 26

def ToMel(f):
	return 1125*np.log(1+(f/700))

def ToFreq(m):
	return 700*(np.exp(m/1125)-1)

def Hamm(elem, length):
	return (0.53836 - 0.46164 * np.cos(2*np.pi*elem/(length-1)))

def GetWeigthCoeffic(n, m, filters_freq):
	begin_filter_m = filters_freq[m - 1]
	center_filter_m = filters_freq[m]
	end_filter_m = filters_freq[m + 1]

	if (n < begin_filter_m or n > end_filter_m):
		return 0
	elif (n >= begin_filter_m and n <= center_filter_m):
		return (n - begin_filter_m)/(center_filter_m - begin_filter_m)
	elif (n >= center_filter_m and n <= end_filter_m):
		return (end_filter_m - n)/(end_filter_m - center_filter_m)

def SplitAudio(data, sr, window_ms, margin_ms):
	print("SplitAudio...")
	partsAudio = []
	stepWindow = int((sr/1000) * window_ms)
	stepMargin = int((sr/1000) * margin_ms)
	count_step = math.ceil(len(data) / stepMargin)
	for i in range(0,len(data),stepMargin):
		if i%100000 == 0:
			print(i)
		partAudio = np.array(data[i:i+stepWindow])
		if (len(partAudio) == stepWindow):
			partsAudio.append(partAudio)
	return partsAudio

def GetMFCC1(partAudio, sr):
	# print("GetMFCCi...")
	# print(len(partAudio))
	low_mel = ToMel(low)
	high_mel = ToMel(high)
	step_mel = (high_mel - low_mel)/(countFilters + 1)
	intervals_mel = [low_mel+i*step_mel for i in range(0,countFilters+2)]
	intervals_freq = [ToFreq(mel) for mel in intervals_mel]

	hamm = np.arange(len(partAudio))
	hamm = [Hamm(hamm[i],len(hamm)) for i in range(len(hamm))]

	# print("fft...")
	partAudio = np.fft.fft(hamm*partAudio)[:len(partAudio//2)]
	partAudio = (np.abs(partAudio)**2)/len(partAudio)

	# print("f...")
	nfft = len(partAudio)
	f = [np.floor((nfft+1)*intervals_freq[i]/sr) for i in range(len(intervals_freq))]
	filters = []
	for m in range(1,countFilters+1):
		filters.append([GetWeigthCoeffic(k, m, f) for k in range(len(partAudio))])

	# for f in filters:
	# 	plt.plot(f)
	# plt.show()

	# print("E...")
	E = []
	for m in range(0,countFilters):
		summa = np.sum(np.array(filters[m]) * np.array(partAudio))
		E.append(np.log(summa))

	# print("mfcc...")
	mfcc = []
	for n in range(countCoeffic):
		summa = 0
		for m in range(countFilters):
			summa += E[m] * np.cos(np.pi*n*(m+0.5)/countFilters)
		mfcc.append(summa)
	return mfcc

def GetMFCC(partsAudio, sr):
	mfccs = []
	for part in partsAudio:
		mfccs.append([GetMFCC1(part,sr),part])
	print(np.array(mfccs).shape)
	return mfccs


def ExtractVoices(data, sr):
	stepWindow = int((sr/1000) * 200)
	partData = data[0:stepWindow]
	mu = np.sum(partData)/stepWindow
	sigma = np.sqrt(np.sum([(partData[i]-mu)**2 for i in range(stepWindow)])/stepWindow)
	data = [data[i] - 0.95*data[i-1] for i in range(1,len(data))]
	partsAudio = SplitAudio(data, sr, 20, 20)
	needParts = []
	for partAudio in partsAudio:
		p = [(np.absolute(partAudio[i] - mu)/sigma) > 3 for i in range(len(partAudio))]
		T = 0
		F = 0
		for e in p:
			if e:
				T += 1
			else:
				F += 1
		if T >= len(p)//2:
			needParts.append(partAudio)
	return np.array(needParts).flatten()

def Dist(v1,v2):
	return np.sum((v1-v2)**2)**0.5

def Preparation(X):
	X = np.array(X)
	L = len(X)
	c = [np.sum(X,axis=0)/L]
	D = np.sum([Dist(c[0],X[i]) for i in range(L)])/L
	return c, D

def VectKvant(X, k = 1):
	c, D = Preparation(X)
	for i in range(k):
		c.append([])
	# np.resize(c,len(c)*2)
	eps = 0.01
	clust = {}
	for i in range(k):
		c[i] = c[i] * (1 - eps)
		clust[i] = []
		c[i + k] = c[i] * (1 + eps)
		clust[i + k] = []
	k *= 2
	m = 0
	
	D__ = D
	while True:
		distances = []
		for i in range(k):
			clust[i] = []
		for xi in X:
			distance = []
			for ci in c:
				distance.append(Dist(ci,xi))
			distances.append(distance)

		for i in range(len(distances)):
			indexMinDist = [j for j, d in enumerate(distances[i]) if d == np.min(distances[i])][0]
			clust[indexMinDist].append(X[i])

		for i in range(k):
			c[i] = np.sum(clust[i],axis=0)/len(clust[i])
		m += 1
		summa = 0
		for i in range(k):
			for v in clust[i]:
				summa += Dist(v,c[i])
		D_ = summa / len(X)
		print(D_,D__,eps)
		if not ((D__ - D_)/D_ > eps):
			break
		D__ = D_
	
	D = D_
	return c, clust

data,sr = librosa.load(path+name)
# voicesParts = ExtractVoices(data, sr)
# librosa.output.write_wav(path + "Voices" + name, voicesParts, sr)

partsAudio = SplitAudio(data, sr, 25, 10)
# test = librosa.feature.mfcc(data,sr,n_mfcc=countCoeffic, hop_length=3060)

# mfccs = GetMFCC(partsAudio, sr)
mfccs = []
for part in partsAudio:
	mfcc = librosa.feature.mfcc(part, sr, n_mfcc=countCoeffic)
	mfcc = np.sum(mfcc,axis=0)/len(mfcc)
	mfccs.append([mfcc,part])

print(len(partsAudio))
mfccs2 = [mfccs[i][0] for i in range(len(mfccs))]
print(len(mfccs2))

c, clust = VectKvant(mfccs2)
# c, clust = VectKvant(mfccs2)

for i in range(len(clust)):
	for j in range(len(clust[i])):
		clust[i][j] =[mfccs[k][1] for k in range(len(mfccs)) if list(mfccs[k][0]) == list(clust[i][j])][0]

for i in range(len(clust)):
	clust[i] = np.array(clust[i]).flatten()

max_len = np.max([len(clust[i]) for i in range(len(clust))])
max_clust = [clust[i] for i in range(len(clust)) if len(clust[i]) == max_len][0]


librosa.output.write_wav(path + "Test" + name, max_clust, sr)

for i in range(len(clust)):
	print(i," : ",len(clust[i]))


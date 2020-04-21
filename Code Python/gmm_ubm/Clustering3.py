import librosa
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import distance
import matplotlib.pyplot as plt

path = 'C:/Users/Ibrag/Desktop/Diplom/Test5/Audio/'
name = 'Presenter_FilteredAudiotest5.wav'


class ModelDictor:
    def __init__(self, w, mu, sigma):
        self.w = w
        self.mu = mu
        self.sigma = sigma

    def GetP(self, data):
        T = len(data)
        summa = 0
        for t in range(T):
            P = 0
            for i in range(len(self.w)):
                P += self.w[i] * self.GetPlotnost(i, data[t])
            logP = np.log(P)
            summa += logP
        return summa

    def GetAposterior(self, i, x):
        # print("GetAposterior... : ",i)
        chisl = self.w[i] * self.GetPlotnost(i, x)
        znam = np.sum([self.w[k] * self.GetPlotnost(k, x) for k in range(len(self.w))])
        return chisl / znam

    def GetPlotnost(self, i, x):
        a0 = (2 * np.pi) ** (len(x) // 2)
        a1 = np.linalg.det(self.sigma[i]) ** 0.5
        a = 1 / (a0 * a1)
        b0 = np.array(x) - self.mu[i]
        b1 = np.linalg.inv(self.sigma[i])
        b2 = np.matmul(b0, b1)
        b = np.vdot(b2, b0)
        return a * np.exp(-b / 2)

    def UpdateData(self, data):
        T = len(data)
        for i in range(len(self.w)):
            print("w : ", i)
            l = []
            print("T : ", T)
            for t in range(T):
                l.append(self.GetAposterior(i, data[t]))
            self.w[i] = np.sum(l) / T
        print(self.w)
        for i in range(len(self.mu)):
            print("mu : ", i)
            chisl = [self.GetAposterior(i, data[t]) * data[t] for t in range(T)]
            chisl = np.sum(chisl, axis=0)
            znam = np.sum([self.GetAposterior(i, data[t]) for t in range(T)])
            self.mu[i] = chisl / znam
        print(self.mu)

    # for i in range(len(self.sigma)):
    # 	print("sigma : ",i)
    # 	chisl = (self.GetAposterior(i, data[t])*(data[t] - self.mu[i])[:,None]*(data[t] - self.mu[i]) for t in range(T))
    # 	chisl = np.sum(chisl, axis=0)
    # 	znam = np.sum([self.GetAposterior(i, data[t]) for t in range(T)])
    # 	self.sigma[i] = chisl/znam
    # print(self.sigma)

    def fit(self, data):
        print("fit...")
        T = len(data)
        p = 0.001
        b = True

        d = []

        m = 0
        while np.sum(d) > 0 or b:
            print("m = ", m)
            self.w_p = self.w
            self.mu_p = self.mu
            self.sigma_p = self.sigma

            print("Update...")
            self.UpdateData(data)
            print("End...")
            d0 = [np.abs(self.w[i] - self.w_p[i]) for i in range(len(self.w))]
            print("d_w : ", d0)
            d0 = [e > p for e in d0]
            d1 = [np.abs(self.mu[i] - self.mu_p[i]) for i in range(len(self.mu))]
            print("d_mu : ", d1)
            d1 = [e > p for e in d1]
            d = [d0[i] and d1[i] for i in range(len(self.w))]
            print("d_all = ", d)
            m += 1
            b = False
        return m


def CountClusters(characteristics):
    K = range(1, 20)
    KM = (KMeans(n_clusters=k).fit(characteristics) for k in K)
    centroids = (k.cluster_centers_ for k in KM)

    D_k = (distance.cdist(characteristics, cent, 'euclidean') for cent in centroids)

    dist = (np.min(D, axis=1) for D in D_k)
    avgWithinSS = [np.sum(d) / characteristics.shape[0] for d in dist]
    plt.plot(K, avgWithinSS, 'b*-')
    plt.grid(True)
    plt.show()


def GetCharacteristics(data, sr, hop_length=None, n_mfcc=None):
    if n_mfcc != None:
        if hop_length != None:
            mfcc = librosa.feature.mfcc(y=data, sr=sr, hop_length=int(hop * sr), n_mfcc=n_mfcc)
        else:
            mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=n_mfcc)
    else:
        mfcc = librosa.feature.mfcc(y=data, sr=sr)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
    stacked = np.vstack((mfcc, mfcc_delta, mfcc_delta2))
    return stacked.T


hop = 0.02
n_mfcc = 16
data, sr = librosa.load(path + name)

characteristics = GetCharacteristics(data, sr, hop, n_mfcc)
print(characteristics.shape)
n_clusters = 4
models = {}
clusters = {}

resClusters = KMeans(n_clusters=n_clusters).fit(characteristics)
centroids = resClusters.cluster_centers_
resClusters = resClusters.predict(characteristics)

for i in range(n_clusters):
    clusters[i] = [characteristics[j] for j in range(len(characteristics)) if resClusters[j] == i]

all_sigma_begin = [np.cov(clusters[i], rowvar=False) for i in range(n_clusters)]
# for i in range(len(all_sigma_begin)):
# 	for j in range(len(all_sigma_begin[i])):
# 		for k in range(len(all_sigma_begin[i][j])):
# 			if j != k:
# 				all_sigma_begin[i][j][k] = 0

w = [len(clusters[i]) / len(characteristics) for i in range(n_clusters)]

print("fit0...")
print("w = ", w)
print("mu = ", centroids)
print("sigma = ", all_sigma_begin)
models[0] = ModelDictor(np.array(w), np.array(centroids), np.array(all_sigma_begin))
models[0].fit(np.array(characteristics))

partData = data[sr * 7:sr * 8]
characteristics2 = GetCharacteristics(partData, sr, hop, n_mfcc)

print("fit1...")
models[1] = ModelDictor(models[0].w, models[0].mu, models[0].sigma)
models[1].UpdateData(np.array(characteristics2))
r = 16
alfa = [models[1].w[i] / (models[1].w[i] + r) for i in range(len(models[1].w))]
models[1].w = np.array([alfa[i] * models[1].w[i] + (1 - alfa[i]) * models[1].w[i] for i in range(len(models[1].w))])
models[1].mu = np.array([alfa[i] * models[1].mu[i] + (1 - alfa[i]) * models[1].mu[i] for i in range(len(models[1].w))])

partsData = []
time_ms = 500
time_s = time_ms / 1000

print("Decomposition...")
step = int(sr * time_s)
i = 0
while i < len(data):
    if i + step <= len(data):
        partsData.append(data[i:int(i + step)])
        i += step
    else:
        break

print("res1...")
res1 = []
for part in partsData:
    characteristics3 = GetCharacteristics(part, sr, n_mfcc=n_mfcc)
    S = [models[i].GetP(characteristics3) for i in range(len(models))]
    S1 = np.max(S)
    if S[1] == S1:
        res1.append(part)

res1 = np.array(res1).flatten()
librosa.output.write_wav(path + "Test_" + name, res1, sr)

import librosa
import numpy as np
import math
import random


def getDistMalahonobis(A, B, R):
    R0 = np.dot(np.transpose(A - B), np.linalg.inv(R))
    print("R0 : ", R0)
    print("inv : ", np.linalg.inv(R))
    R1 = np.dot(R0, A - B)
    print("A - B : ", np.array(A - B))
    print("R1 : ", R1)
    return R1

getDistMalahonobis(np.array([1, 2]), np.array([10,22]), np.array([[1,2],[3,4]]))

def GetCharacteristics(data, sr, hop_length=None, n_mfcc=None):
    if n_mfcc is not None:
        if hop_length is not None:
            mfcc = librosa.feature.mfcc(y=data, sr=sr, hop_length=hop_length, n_mfcc=n_mfcc)
        else:
            mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=n_mfcc)
    else:
        mfcc = librosa.feature.mfcc(y=data, sr=sr)
#    mfcc_delta = librosa.feature.delta(mfcc)
#    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
#    stacked = np.vstack((mfcc, mfcc_delta, mfcc_delta2))
#    return stacked.T
    return mfcc

def SplitAudio(data, sr, window_ms, margin_ms):
    print("SplitAudio...")
    partsAudio = []
    stepWindow = int((sr / 1000) * window_ms)
    stepMargin = int((sr / 1000) * margin_ms)
    count_step = math.ceil(len(data) / stepMargin)
    for i in range(0, len(data), stepMargin):
        partAudio = np.array(data[i:i + stepWindow])
        if len(partAudio) == stepWindow:
            partsAudio.append(partAudio)
    return partsAudio


path = 'C:/Users/Ibrag/Downloads/Telegram Desktop/'
name = 'test.wav'
data, sr = librosa.load(path + name)
partsAudio = SplitAudio(data, sr, 100, 100)
characteristics = np.array([np.array(GetCharacteristics(part, sr, n_mfcc=16)).flatten() for part in partsAudio])

k = 2
Y = np.array(characteristics)
n = Y.shape[0]
q = Y.shape[1]
eps = 0.01
Q = 10

R = np.array([np.eye(q) for i in range(k)])
C = np.random.uniform(1, 10, (q, k))
W = np.array([1/k for i in range(k)])
D = np.zeros(n*k).reshape(n, k)
P = np.zeros(n*k).reshape(n, k)
X = np.zeros(n*k).reshape(n, k)

llh = 1e+2
d_llh = llh

while d_llh >= eps and Q <= 10:
    C_ = np.zeros(C.shape)
    R_ = np.zeros(R.shape)
    W_ = np.zeros(W.shape)
    llh = 0
    sump = np.zeros(n)
    for i in range(n):
        sump[i] = 0
        for j in range(k):
            D[i][j] = getDistMalahonobis(Y[i], C[:, j], R[j])
            P[i][j] = W[j] * np.exp(-D[i][j]/2) / np.sqrt(pow(2*np.pi, q)*np.linalg.det(R[j]))
            sump[i] += P[i][j]
        X[i] = P[i]/sump[i]
        llh += np.log(sump[i])
        C_ += Y[i][:, None] * X[i]
        W_ += X[i]

    for j in range(k):
        C[:, j] = C_[:, j]/W_[j]
        for i in range(n):
            R_[j] += (Y[i] - C[:, j]) * X[i][j] * np.transpose(Y[i] - C[:, j])
        R[j] = R_[j]/n
        W = W_/n

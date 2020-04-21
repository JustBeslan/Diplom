import pickle
import librosa
import numpy as np
from sklearn import preprocessing
import os
from sklearn.mixture import GaussianMixture
import pandas as pd


def getMFCC(data, sr):
    mfcc = librosa.feature.mfcc(data, sr, n_mfcc=13, n_fft=512, hop_length=int(sr * 0.025)).T
    print(np.array(mfcc).shape)
    mfcc = preprocessing.scale(mfcc)
    return mfcc


gender = "male"
path_train = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/train_data/youtube/" + gender + "/"
path_save_model = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/"

features = []
for file in os.listdir(path_train):
    data, sr = librosa.load(path_train + file)
    mfcc = getMFCC(data, sr)
    print(np.array(mfcc).shape)
    for e in mfcc:
        features.append(e)

gmm = GaussianMixture(n_components=8, max_iter=200, covariance_type='diag', n_init=5)
print(np.array(features).shape)
gmm.fit(features)
pickle.dump(gmm, open(path_save_model + "L" + gender + ".gmm", "wb"))




import os
import pickle
import librosa
import numpy as np
from sklearn import preprocessing


def getMFCC(data, sr):
    mfcc = librosa.feature.mfcc(data, sr, n_mfcc=13, n_fft=512, hop_length=int(sr * 0.025)).T
    print(np.array(mfcc).shape)
    mfcc = preprocessing.scale(mfcc)
    return mfcc


genders = ["male", "female"]
gender = genders[1]
path_test = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/test_data/AudioSet/" + gender + "_clips/"
model_path = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/"
models = [pickle.load(open(model_path + "L" + gender_ + ".gmm", 'rb')) for gender_ in genders]

for file in os.listdir(path_test):
    data, sr = librosa.load(path_test + file)
    mfcc = getMFCC(data, sr)
    log_likelihood = np.zeros(len(models))
    for i in range(len(models)):
        gmm = models[i]  # checking with each model one by one
        log_likelihood[i] = np.array(gmm.score(mfcc))
    winner = np.argmax(log_likelihood)
    print("Res : ", genders[winner])

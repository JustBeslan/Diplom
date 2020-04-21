import os
import pickle
import numpy as np
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn import preprocessing
from test999.test2.speakerfeatures import extract_features


def SplitAudio(data, sr, window_ms, margin_ms):
    print("SplitAudio...")
    partsAudio = []
    stepWindow = int((sr / 1000) * window_ms)
    stepMargin = int((sr / 1000) * margin_ms)
    for i in range(0, len(data), stepMargin):
        partAudio = np.array(data[i:i + stepWindow])
        if len(partAudio) == stepWindow:
            partsAudio.append(partAudio)
    return partsAudio


def get_MFCC(sr, audio):
    features = mfcc.mfcc(audio, sr, 0.025, 0.01, 13, appendEnergy=False)
    feat = np.asarray(())
    for i in range(features.shape[0]):
        temp = features[i, :]
        if np.isnan(np.min(temp)):
            continue
        else:
            if feat.size == 0:
                feat = temp
            else:
                feat = np.vstack((feat, temp))
    features = feat
    features = preprocessing.scale(features)
    return features


def getGender(audio, sr):
    modelpath = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/"

    gmm_files = [os.path.join(modelpath, fname) for fname in
                 os.listdir(modelpath) if fname.endswith('.gmm')]
    models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
    genders = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
    features = get_MFCC(sr, audio)
    log_likelihood = np.zeros(len(models))
    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(features))
        log_likelihood[i] = scores.sum()
    winner = np.argmax(log_likelihood)
    res = genders[winner]
    return res


def getHuman(audio, sr):
    modelpath = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset2/speaker_models/"
    gmm_files = [os.path.join(modelpath, fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]

    models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
    speakers = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
    vector = extract_features(audio, sr)
    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores

    winner = np.argmax(log_likelihood)
    return speakers[winner]


path = "C:/Users/Ibrag/Desktop/Diplom/Test6/Audio/"
name = "FilteredAudiotest6.wav"

sr, audio = read(path + name)
start_s = 3
part = audio[sr * start_s:int(sr * (start_s + 3))]
gender = getGender(part, sr)
human = getHuman(part, sr)
print(human)

partsAudio = SplitAudio(audio, sr, 100, 100)
for i, part in enumerate(partsAudio):
    print(" : human - ", getHuman(part, sr))



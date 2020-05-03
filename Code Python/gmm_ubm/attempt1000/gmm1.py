import python_speech_features as psf
import scipy.io.wavfile as wav
import numpy as np
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture


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


def extract_features(data, sr):
    mfcc = psf.mfcc(data, sr, split_ms/1000, margin_ms/1000, 20, appendEnergy=True)
    mfcc = preprocessing.scale(mfcc)
    delta = psf.delta(mfcc, 2)
    return np.hstack((mfcc, delta))


def get_statistics(L):
    dictionary = {}
    for a in L:
        if dictionary.get(a) is None:
            dictionary[a] = 1
        else:
            dictionary[a] += 1
    return dictionary


def train_gmm(data):
    y = np.ones(data.shape[0])
    gmm = GaussianMixture(n_components=8, max_iter=200, covariance_type='diag', n_init=10)
    gmm.fit(data, y)
    # pickle_file = 'presenter.gmm'
    # pickle.dump(gmm, open(path + 'Models_Humans/' + pickle_file, 'wb'))
    return gmm


path = "C:/Users/Ibrag/Desktop/Diplom/Videos/Test3/Audio/"
name = "voices.wav"
split_ms = 50
margin_ms = 25
sr, data = wav.read(path + name)
mfcc_feat = extract_features(data, sr)
parts = SplitAudio(data, sr, split_ms, margin_ms)

put = int((split_ms-margin_ms) * sr/1000)
start_presenter_ms = 17000
end_presenter_ms = 18000

parts_presenter = parts[int(start_presenter_ms / split_ms):int(end_presenter_ms / split_ms)]
mfcc_feat_presenter = mfcc_feat[int(start_presenter_ms / split_ms):int(end_presenter_ms / split_ms)]
print(np.array(parts_presenter).shape, np.array(mfcc_feat_presenter).shape)

gmm = train_gmm(mfcc_feat_presenter)
scores = [gmm.score(mfcc_feat[i:i + 1]) for i in range(0, len(mfcc_feat), 1)]

predicts = [gmm.predict(mfcc_feat[i:i + 1]) for i in range(0, len(mfcc_feat), 1)]
stat_predicts = get_statistics(np.array(predicts).flatten())
max_value = np.max(list(stat_predicts.values()))
max_key = -1
print(stat_predicts)
for key in stat_predicts.keys():
    if stat_predicts.get(key) == max_value:
        max_key = key
need_parts1 = [parts[i] for i in range(0, len(parts)) if predicts[i] != max_key or scores[i] < -20000]
need_parts2 = [parts[i] for i in range(0, len(parts)) if predicts[i] == max_key or scores[i] > -20000]
wav.write(path + "voices1.wav", sr, np.array(need_parts1).flatten())
wav.write(path + "voices2.wav", sr, np.array(need_parts2).flatten())


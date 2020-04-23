import os
import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM
import python_speech_features as mfcc
from sklearn import preprocessing


class GenderClassificatory:

    def __init__(self, path):
        self.pathGenderModelsDirs = path + "Models_Genders/"
        if not os.path.exists(self.pathGenderModelsDirs):
            os.makedirs(self.pathGenderModelsDirs)

    def Train(self, gender, pathTrainData):
        # self.pathTrainData = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/train_data/youtube/" + gender + "/"
        # self.pathSaveModel = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/"
        files = [os.path.join(pathTrainData, f) for f in os.listdir(pathTrainData) if f.endswith('.wav')]
        features = np.asarray(())
        for f in files:
            sr, audio = read(f)
            vector = self.get_MFCC(sr, audio)
            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))
        gmm = GMM(n_components=12, max_iter=200, covariance_type='diag', n_init=5)
        gmm.fit(np.array(features))
        picklefile = gender + ".gmm"
        pickle.dump(gmm, open(self.pathGenderModelsDirs + picklefile, "wb"))
        print('modeling completed for gender:', picklefile)

    def get_MFCC(self, sr, audio):
        features = mfcc.mfcc(audio, sr, 0.025, 0.01, 13, appendEnergy=False)
        features = preprocessing.scale(features)
        return features

    def classification(self, sr, audio):
        # modelpath = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset1/pygender/"
        gmm_files = [os.path.join(self.pathGenderModelsDirs, fname) for fname in
                     os.listdir(self.pathGenderModelsDirs) if fname.endswith('.gmm')]
        models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
        genders = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
        features = self.get_MFCC(sr, audio)
        log_likelihood = np.zeros(len(models))
        for i in range(len(models)):
            gmm = models[i]
            scores = np.array(gmm.score(features))
            log_likelihood[i] = scores.sum()
        winner = np.argmax(log_likelihood)
        return genders[int(winner)]
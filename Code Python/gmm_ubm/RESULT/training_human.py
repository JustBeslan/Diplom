import os
import pickle
import numpy as np
from scipy.io.wavfile import read
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture as GMM
import python_speech_features as feature


class HumanClassificatory:

    def __init__(self, path):
        self.pathHumansModelsDirs = path + "Models_Humans/"
        if not os.path.exists(self.pathHumansModelsDirs):
            os.makedirs(self.pathHumansModelsDirs)

    def Train(self, pathTrainData=None, x=None, sr=None):
        # source = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset2/development_set/"
        # dest = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset2/speaker_models/"
        if pathTrainData is not None:
            features = np.asarray(())
            for trainFile in os.listdir(pathTrainData):
                sr, audio = read(pathTrainData + trainFile)
                vector = self.ExtractFeatures(audio, sr)
                if features.size == 0:
                    features = vector
                else:
                    features = np.vstack((features, vector))
            picklefile = "not_presenter.gmm"
        else:
            features = self.ExtractFeatures(x, sr)
            picklefile = "presenter.gmm"
        gmm = GMM(n_components=16, max_iter=200, covariance_type='full', n_init=3)
        gmm.fit(features)
        pickle.dump(gmm, open(self.pathHumansModelsDirs + picklefile, 'wb'))
        print('+ modeling completed for speaker:', picklefile, " with data point = ", features.shape)

    def ExtractFeatures(self, audio, sr):
        mfcc_feat = feature.mfcc(audio, sr, 0.025, 0.01, 20, appendEnergy=True)
        mfcc_feat = preprocessing.scale(mfcc_feat)
        delta = feature.delta(mfcc_feat, 2)
        combined = np.hstack((mfcc_feat, delta))
        return combined

    def Classification(self, sr, audio):
        # modelpath = "C:/Users/Ibrag/Desktop/Diplom/Datasets/Dataset2/speaker_models/"
        gmm_files = [os.path.join(self.pathHumansModelsDirs, fname) for fname in
                     os.listdir(self.pathHumansModelsDirs) if fname.endswith('.gmm')]

        models = [pickle.load(open(fname, 'rb')) for fname in gmm_files]
        speakers = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]
        vector = self.ExtractFeatures(audio, sr)
        log_likelihood = np.zeros(len(models))

        for i in range(len(models)):
            gmm = models[i]
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores

        winner = np.argmax(log_likelihood)
        return speakers[int(winner)]

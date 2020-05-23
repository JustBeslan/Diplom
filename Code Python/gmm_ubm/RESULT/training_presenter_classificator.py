import python_speech_features as psf
import numpy as np
from sklearn.mixture import GaussianMixture
import scipy.io.wavfile as wav
from RESULT.OtherProcessing import split_audio


class ClassificatorPresenter:
    def __init__(self, path_voices, name_voices, interval_ms, window_ms, margin_ms):
        self.window_ms = window_ms
        self.margin_ms = margin_ms
        self.sr, data = wav.read(filename=path_voices + name_voices)
        self.split_data = split_audio(data=data,
                                      sr=self.sr,
                                      window_ms=window_ms,
                                      margin_ms=margin_ms)
        self.frame_length = len(self.split_data[0])
        self.intervals_split_data = [[i * window_ms, (i + 1) * window_ms] for i in range(len(self.split_data))]
        self.features_split_data = [self.ExtractFeatures(part_split_data) for part_split_data in self.split_data]
        self.indexes_intervals_presenter = [i for i, interval in enumerate(self.intervals_split_data)
                                            if interval[0] >= interval_ms[0] and interval[1] <= interval_ms[1]]
        features_intervals_presenter = [feature for i, feature in enumerate(self.features_split_data)
                                        if i in self.indexes_intervals_presenter]
        self.features_presenter = np.vstack(tuple(features_intervals_presenter))
        self.gmm_presenter = self.train_gmm(self.features_presenter)

    def ExtractFeatures(self, data):
        window_s = self.window_ms / 1000
        margin_s = self.margin_ms / 1000
        mfcc = psf.mfcc(signal=data,
                        samplerate=self.sr,
                        winlen=window_s,
                        winstep=margin_s,
                        numcep=20,
                        appendEnergy=True,
                        nfft=self.frame_length)
        delta = psf.delta(feat=mfcc,
                          N=2)
        return np.hstack((mfcc, delta))

    def train_gmm(self, feature_presenter):
        feature = feature_presenter
        for i in range(5):
            np.append(feature, feature_presenter, axis=0)
        gmm = GaussianMixture(n_components=8,
                              max_iter=200,
                              covariance_type='diag',
                              n_init=10)
        gmm.fit(X=feature)
        return gmm

    def get_statistics(self, list_a):
        dictionary = {}
        for a in list_a:
            if dictionary.get(a) is None:
                dictionary[a] = 1
            else:
                dictionary[a] += 1
        return dictionary

    def Classification(self):
        scores_split_data = [self.gmm_presenter.score(X=feature_split_data) for feature_split_data
                             in self.features_split_data]

        scores_intervals_presenter = [score_split_data for i, score_split_data in enumerate(scores_split_data)
                                      if i in self.indexes_intervals_presenter]

        result = [i for i in range(len(scores_split_data))
                  if not np.min(scores_intervals_presenter) <= scores_split_data[i] <= np.max(scores_intervals_presenter)]
        return result


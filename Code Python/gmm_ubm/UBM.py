from Feature import Feature_
from sklearn.mixture import GaussianMixture
import librosa
from sklearn import preprocessing
import numpy as np
import pickle

class UBM_:
	
	def __init__(self, dataAudio, sr, pathAudio):
		self.pathAudio = pathAudio
		self.dataAudio = dataAudio
		self.sr = sr
		ubm_features = self.CreateMFCC()
		self.ubm = self.CreateUBM(ubm_features)

	def CreateMFCC(self):

		features = Feature_()

		FEATURES_FROM_FILE = False
		feature_file_name = self.pathAudio+'data/features_{0}.pkl'.format(features.N_MFCC)

		if FEATURES_FROM_FILE:
			ubm_features=pickle.load(open(feature_file_name, 'rb'))
		else:
			ubm_features = features.extract_features(np.array(self.dataAudio), self.sr, window=features.N_FFT, hop=features.HOP_LENGTH, n_mfcc=features.N_MFCC)
			ubm_features = preprocessing.scale(ubm_features)
			pickle.dump(ubm_features, open(feature_file_name, "wb"))
		return ubm_features

	def CreateUBM(self, ubm_features):

		N_COMPONENTS = 16 # number of gaussians
		COVARINACE_TYPE = 'full' # cov type for GMM

		UBM_FROM_FILE = False
		ubm_file_name = self.pathAudio+'data/ubm_{0}_{1}_{2}MFCC.pkl'.format(N_COMPONENTS, COVARINACE_TYPE, Feature_().N_MFCC)

		if UBM_FROM_FILE:
			ubm=pickle.load(open(ubm_file_name, 'rb'))
		else:
			ubm = GaussianMixture(n_components = N_COMPONENTS, covariance_type = COVARINACE_TYPE)
			ubm.fit(ubm_features)
			pickle.dump(ubm, open(ubm_file_name, "wb"))
		print(ubm.score(ubm_features))
		return ubm

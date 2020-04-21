import librosa
import numpy as np

class Feature_:

	N_MFCC = 32 # number of MFCC to extract
	N_FFT = 0.032  # length of the FFT window in seconds
	HOP_LENGTH = 0.010 # number of samples between successive frames in seconds

	def extract_features(self, y, sr, window, hop, n_mfcc):
		mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=int(hop*sr), n_fft=int(window*sr), n_mfcc=n_mfcc, dct_type=2)
		mfcc_delta = librosa.feature.delta(mfcc)
		mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
		stacked = np.vstack((mfcc, mfcc_delta, mfcc_delta2))
		return stacked.T

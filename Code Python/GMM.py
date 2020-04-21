from IPython.display import clear_output
from Feature import Feature_
from sklearn import preprocessing
import librosa
import copy
import numpy as np

class GMM_:
	def __init__(self, pathAudio, ubm):
		self.pathAudio = pathAudio
		self.ubm = ubm
		self.superVector = self.CreateSuperVector()

	def CreateSuperVector(self):

		feature = Feature_()

		superVectors = []
		# возьмём сегменты от chunk-000 до chunk-100
		for i in range(101):
			clear_output(wait=True)
			fname=self.pathAudio+'data/chunks/chunk-%003d.wav' % (i,)
			print('UBM MAP adaptation for {0}'.format(fname))
			dataPartAudio, srPartAudio = librosa.load(fname, sr=None)
			features = feature.extract_features(dataPartAudio, srPartAudio, window=feature.N_FFT, hop=feature.HOP_LENGTH, n_mfcc=feature.N_MFCC)
			features = preprocessing.scale(features)
			gmm = copy.deepcopy(self.ubm)
			gmm = self.map_adaptation(gmm, features, max_iterations=100, relevance_factor=16)
			# print(gmm.means_)
			superVector = gmm.means_.flatten() #получаем супервектор мю
			superVector = preprocessing.scale(superVector)
			superVectors.append(superVector)
		superVectors = np.array(superVectors)
		clear_output()
		print(superVectors.shape)
		return superVectors

	def map_adaptation(self,gmm, data, max_iterations = 300, likelihood_threshold = 1e-20, relevance_factor = 16):
		N = data.shape[0]	#	data = x (matrix)
		D = data.shape[1]	# D = 3
		K = gmm.n_components	#	K = 16
    
		mu_new = np.zeros((K,D))	#	E (vector)
		n_k = np.zeros((K,1))	#	n (vector)
    
		mu_k = gmm.means_	#	mu (vector)
		# cov_k = gmm.covariances_
		# pi_k = gmm.weights_

		old_likelihood = gmm.score(data)
		new_likelihood = 0
		iterations = 0
		while(abs(old_likelihood - new_likelihood) > likelihood_threshold and iterations < max_iterations):
			iterations += 1
			old_likelihood = new_likelihood
			z_n_k = gmm.predict_proba(data)	#	Pr(i|xt,lambdaUBM)	апостериорная вероятность (matrix)
			n_k = np.sum(z_n_k,axis = 0)	#	n (vector)

		for i in range(K):
			temp = np.zeros((1,D))
			for n in range(N):	#	T = N (t = n)
				temp += z_n_k[n][i]*data[n,:]
			# print(temp)
			mu_new[i] = (1/n_k[i])*temp	# E_i(x) = 1/n_i * summa[t=1..T](Pr(i|xt,lambdaUBM)*xt)

		adaptation_coefficient = n_k/(n_k + relevance_factor)		# alfa_i = n_i/(n_i+r)
		for k in range(K):
			mu_k[k] = (adaptation_coefficient[k] * mu_new[k]) + ((1 - adaptation_coefficient[k]) * mu_k[k])	#	mu_i = alfa_i*E_i(x) + (1 - alfa_i)*mu_i
		gmm.means_ = mu_k

		log_likelihood = gmm.score(data)
		new_likelihood = log_likelihood
		print(log_likelihood)
		return gmm

		
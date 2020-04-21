import librosa
import numpy as np
import math
import cmath

class MFCC_:

	partsDataAudio = []

	def __init__(self, countCoefficMFCC):
		self.countCoefficMFCC = countCoefficMFCC
		
	def SplitAudio(self, pathAudio, nameAudio):
		cadr_ms = 30
		overlapped_ms = 10

		dataAudio, sr = librosa.load(pathAudio + nameAudio)
		# self.lengthCadr = int((sr/1000) * cadr_ms)
		self.lengthCadr = 512
		overlapped = int((sr/1000) * overlapped_ms)
		step = self.lengthCadr - overlapped
		for i in range(0,len(dataAudio),step):
			partDataAudio = dataAudio[i:i+self.lengthCadr]
			if len(partDataAudio) == self.lengthCadr:
				self.partsDataAudio.append(partDataAudio)
		print(self.lengthCadr)
		self.windowHamming = np.hamming(self.lengthCadr)

	def FFT(self, x):
		"""A vectorized, non-recursive version of the Cooley-Tukey FFT"""
		x = np.asarray(x, dtype=float)
		N = x.shape[0]

		if np.log2(N) % 1 > 0:
			raise ValueError("size of x must be a power of 2")

		# N_min here is equivalent to the stopping condition above,
		# and should be a power of 2
		N_min = min(N, 32)
	    
		# Perform an O[N^2] DFT on all length-N_min sub-problems at once
		n = np.arange(N_min)	#	= np.array([0..N_min])
		k = n[:, None]	#	transpose
		M = np.exp(-2j * np.pi * n * k / N_min)	#	32x32
		X = np.dot(M, x.reshape((N_min, -1)))	# X(32x16) = M(32x32) * x(32x16)

		# build-up each level of the recursive calculation all at once
		while X.shape[0] < N:	#	512 < 32 ...... 32 !< 32
			X_even = X[:, :int(X.shape[1] / 2)]	#	X_even()
			X_odd = X[:, int(X.shape[1] / 2):]
			factor = np.exp(-1j * np.pi * np.arange(X.shape[0]) / X.shape[0])[:, None]
			X = np.vstack([X_even + factor * X_odd, X_even - factor * X_odd])
		return X.ravel()

	def ToMel(self, f):
		return 1127.01048*math.log1p(1 + (f/700))

	def GetTriangleFilter(self, M, f, s, fLow, fHigh):
		m_f_low = self.ToMel(fLow)
		m_f_high = self.ToMel(fHigh)
		m_f = self.ToMel(f)
		
		m_s_begin = m_f_low + s * ((m_f_high - m_f_low)/(M + 1))
		m_s_end = m_f_low + (s + 2) * ((m_f_high - m_f_low)/(M + 1))
		m_s_center = (m_s_begin + m_s_end)/2

		if (m_f < m_s_begin or m_f >= m_s_end):
			return 0
		elif (m_f >= m_s_begin and m_f < m_s_center):
			return (m_f - m_s_begin)/(m_s_center - m_s_begin)
		elif (m_f >= m_s_center and m_f < m_s_end):
			return (m_s_end - m_f)/(m_s_end - m_s_center)

	def ComputeMFCC(self):
		countFilters = 24
		fLow = 300
		fHigh = 3000

		mfcc = []
		print(len(self.partsDataAudio))
		for i in range(0,len(self.partsDataAudio)):
			print(i)
			F_k = self.FFT(self.partsDataAudio[i])
			F_k_abs = abs(F_k)
			E = []
			for s in range(0,countFilters):
				summa = 0
				for k in range(0,len(F_k)):
					summa += F_k_abs**2*self.GetTriangleFilter(countFilters, F_k[k], s, fLow, fHigh)
				E_s = np.log1p(summa)
				E.append(E_s)
			mfcc_part = []
			for i in range(0,self.countCoefficMFCC):
				mfcc_i = 0
				for m in range(0,len(E)):
					mfcc_i += E[m]*np.cos(np.pi*i*(m+0.5)/len(E))
				mfcc_part.append(mfcc_i)
			mfcc.append(mfcc_part)
		return mfcc

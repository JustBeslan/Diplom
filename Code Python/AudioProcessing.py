from VAD import VAD_
from UBM import UBM_
from GMM import GMM_
from Clustering import Clustering_
from scipy.signal import butter, lfilter
import librosa
import moviepy.editor as mp
import math
import copy

class Audio_Processing:

	SR = 8000 # sample rate

	def __init__(self, path, name):
		self.name = name
		self.pathAudio = path
		self.slice_ms = 500
		self.dataAudio, self.sr = librosa.load(self.pathAudio + self.name, sr=self.SR) # mono=False

	def ToExtractAudioFromVideo(self):
		files = os.listdir(self.path)
		videoclip = mp.VideoFileClip(self.path + files[0])
		audioclip = videoclip.audio
		pathAudio = self.path + "Audio/"
		os.makedirs(pathAudio)
		nameOriginalAudio = "Audio" + files[0]
		audioclip.write_audiofile(pathAudio + nameOriginalAudio, ffmpeg_params=["-ac", "1"])
		self.pathAudio = pathAudio
		self.nameOriginalAudio = nameOriginalAudio

	def FilteringAudio(self):
		dataAudio, sr = librosa.load(self.pathAudio + self.nameOriginalAudio) # mono=False
		step = int((sr/1000) * self.slice_ms)				# Always value parameter slice_ms should be >= 10
		count_step = math.ceil(len(dataAudio) / step)			# This is so time video(step = fs_rate).
		print(count_step)
		#=========Готовим постоянные данные для фильтрации каждой части аудио============
		lowcut = 300
		highcut = 3000
		nyq = 0.5 * sr
		low = lowcut / nyq
		high = highcut / nyq
		b, a = butter(6, [low, high], btype='band')
		#================================================================================
		filteredDataAudio = dataAudio.copy()
		for i in range(0,count_step):
			fromPartAudio = i*step
			toPartAudio = fromPartAudio + step

			partDataAudio = dataAudio[fromPartAudio:toPartAudio]
			filteredPartDataAudio = lfilter(b, a, partDataAudio)
			filteredDataAudio[fromPartAudio:toPartAudio] = filteredPartDataAudio

		self.nameFilteredAudio = self.pathAudio + "Filtered" + self.nameOriginalAudio
		librosa.output.write_wav(self.nameFilteredAudio, filteredDataAudio, sr)

	def Processing(self):
		vad = VAD_(self.dataAudio,self.sr,self.pathAudio)
		ubm = UBM_(self.dataAudio,self.sr,self.pathAudio)
		gmm = GMM_(self.pathAudio,ubm.ubm)
		clusters = Clustering_(gmm.superVector)


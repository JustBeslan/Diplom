import wave
import pickle
import contextlib
import librosa
import numpy as np
import IPython.display as ipd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture
from scipy.spatial.distance import cdist
import webrtcvad
import collections
import copy
import os
from IPython.display import clear_output
from sklearn.cluster import SpectralClustering
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class Frame(object):
	def __init__(self, bytes, timestamp, duration):
		self.bytes = bytes
		self.timestamp = timestamp
		self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
	n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
	offset = 0
	timestamp = 0.0
	duration = (float(n) / sample_rate) / 2.0
	while offset + n < len(audio):
		yield Frame(audio[offset:offset + n], timestamp, duration)
		timestamp += duration
		offset += n

def vad_collector(sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
	num_padding_frames = int(padding_duration_ms / frame_duration_ms)
	ring_buffer = collections.deque(maxlen=num_padding_frames)
	triggered = False

	voiced_frames = []
	for frame in frames:
		is_speech = vad.is_speech(frame.bytes, sample_rate)

	if not triggered:
		ring_buffer.append((frame, is_speech))
		num_voiced = len([f for f, speech in ring_buffer if speech])
		if num_voiced > 0.9 * ring_buffer.maxlen:
			triggered = True
			for f, s in ring_buffer:
				voiced_frames.append(f)
			ring_buffer.clear()
	else:
		voiced_frames.append(frame)
		ring_buffer.append((frame, is_speech))
		num_unvoiced = len([f for f, speech in ring_buffer if not speech])
		if num_unvoiced > 0.9 * ring_buffer.maxlen:
			triggered = False
			yield b''.join([f.bytes for f in voiced_frames])
			ring_buffer.clear()
			voiced_frames = []
	if voiced_frames:
		yield b''.join([f.bytes for f in voiced_frames])

path = '/home/beslan/Diplom/WorkWithVideo6/Audio/'
name = 'Audiotest6.wav'

#читаем сигнал
y, sr = librosa.load(path+name)
#первым шагом делаем pre-emphasis: усиление высоких частот
pre_emphasis = 0.97
y = np.append(y[0], y[1:] - pre_emphasis * y[:-1])

#все что ниже фактически взято с гитхаба webrtcvad с небольшими изменениями
vad = webrtcvad.Vad(2) # агрессивность VAD
audio = np.int16(y/np.max(np.abs(y)) * 32767)

# frames = frame_generator(10, audio, sr)
# frames = list(frames)
# segments = vad_collector(sr, 50, 200, vad, frames)

# if not os.path.exists(path+'chunks'): os.makedirs(path+'chunks')
# for i, segment in enumerate(segments):
#     chunk_name = path+'chunks/chunk-%003d.wav' % (i,)
#     # vad добавляет в конце небольшой кусочек тишины, который нам не нужен
#     write_wave(chunk_name, segment[0: len(segment)-int(100*sr/1000)], sr)

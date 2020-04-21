import numpy as np
import webrtcvad
import os
import contextlib
import wave
import collections

class Frame:
	def __init__(self, bytes, timestamp, duration):
		self.bytes = bytes
		self.timestamp = timestamp
		self.duration = duration

class VAD_:
	def __init__(self, dataAudio, sr, pathAudio):
		self.dataAudio = dataAudio
		self.sr = sr
		self.pathAudio = pathAudio
		self.VADAudio()
		
	def VADAudio(self):
		#первым шагом делаем pre-emphasis: усиление высоких частот
		pre_emphasis = 0.97
		self.dataAudio = np.append(self.dataAudio[0], self.dataAudio[1:] - pre_emphasis * self.dataAudio[:-1])

		#все что ниже фактически взято с гитхаба webrtcvad с небольшими изменениями
		vad = webrtcvad.Vad(2) # агрессивность VAD
		audio = np.int16(self.dataAudio/np.max(np.abs(self.dataAudio)) * 32767)

		frames = self.frame_generator(10, audio, self.sr)
		frames = list(frames)
		segments = self.vad_collector(self.sr, 50, 200, vad, frames)

		if not os.path.exists(self.pathAudio+'data/chunks'):
			os.makedirs(self.pathAudio+'data/chunks')
		for i, segment in enumerate(segments):
			chunk_name = self.pathAudio+'data/chunks/chunk-%003d.wav' % (i,)
			# vad добавляет в конце небольшой кусочек тишины, который нам не нужен
			self.write_wave(chunk_name, segment[0: len(segment)-int(100*self.sr/1000)], self.sr)

	def frame_generator(self,frame_duration_ms, audio, sample_rate):
		n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
		offset = 0
		timestamp = 0.0
		duration = (float(n) / sample_rate) / 2.0
		while offset + n < len(audio):
			yield Frame(audio[offset:offset + n], timestamp, duration)
			timestamp += duration
			offset += n

	def vad_collector(self,sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
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

	def write_wave(self,path, audio, sample_rate):
		with contextlib.closing(wave.open(path, 'wb')) as wf:
			wf.setnchannels(1)
			wf.setsampwidth(2)
			wf.setframerate(sample_rate)
			wf.writeframes(audio)


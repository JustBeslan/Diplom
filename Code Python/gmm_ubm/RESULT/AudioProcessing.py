import os
import math
import librosa
import numpy as np
import moviepy.editor as mp
from scipy.signal import butter, lfilter
from tkinter import END
from RESULT.OtherProcessing import split_audio


class Audio_Processing:
    SR = 16000
    slice_ms = 25
    intervals_silence = []
    intervals_voices = []

    def __init__(self, path_video, name_video, messages):
        self.messages = messages
        self.nameVideo = name_video
        self.pathVideo = path_video

        self.to_extract_audio_from_video()
        self.messages.insert(END, "Видео загружено\n")
        self.messages.insert(END, 'Нажмите "Далее"\n')

    def to_extract_audio_from_video(self):
        self.messages.insert(END, "Извлекается аудио из видео...\n")
        video_file_clip = mp.VideoFileClip(filename=self.pathVideo + self.nameVideo)
        audio_clip = video_file_clip.audio
        path_audio = self.pathVideo + "Audio/"
        if not os.path.exists(path_audio):
            os.makedirs(name=path_audio)
        name_original_audio = "Audio" + str(self.nameVideo).split(".")[0] + ".wav"
        audio_clip.write_audiofile(filename=path_audio + name_original_audio,
                                   ffmpeg_params=["-ac", "1"])
        self.path_audio = path_audio
        self.name_original_audio = name_original_audio
        self.messages.insert(END, "Извлечение завершено\n")

    def filtering_audio(self):
        self.messages.insert(END, "Идет фильтрация извлеченного аудио...\n")
        data_audio, sr = librosa.load(path=self.path_audio + self.name_original_audio,
                                      sr=self.SR)  # mono=False
        step = int((sr / 1000) * self.slice_ms)  # Always value parameter slice_ms should be >= 10
        count_step = math.ceil(len(data_audio) / step)  # This is so time video(step = fs_rate).
        # =========Готовим постоянные данные для фильтрации каждой части аудио============
        low_cut = 300
        high_cut = 3000
        nyq = 0.5 * sr
        low = low_cut / nyq
        high = high_cut / nyq
        b, a = butter(6, [low, high], btype='band')
        # ================================================================================
        self.filtered_data_audio = data_audio.copy()
        for i in range(0, count_step):
            from_part_audio = i * step
            to_part_audio = from_part_audio + step
            part_data_audio = data_audio[from_part_audio:to_part_audio]
            filtered_part_data_audio = lfilter(b=b,
                                               a=a,
                                               x=part_data_audio)
            self.filtered_data_audio[from_part_audio:to_part_audio] = filtered_part_data_audio
        self.nameFilteredAudio = "Filtered_" + self.name_original_audio
        librosa.output.write_wav(path=self.path_audio + self.nameFilteredAudio,
                                 y=self.filtered_data_audio,
                                 sr=self.SR)
        self.messages.insert(END, "Фильтрация аудио завершена\n")

    def ExtractVoices(self, data, sr):
        self.messages.insert(END, "Идет извлечение голоса...\n")
        stepWindow = int((sr / 1000) * 200)
        partData = data[0:stepWindow]
        mu = np.sum(partData) / stepWindow
        sigma = np.sqrt(np.sum([(partData[i] - mu) ** 2 for i in range(stepWindow)]) / stepWindow)
        data = [data[i] - 0.95 * data[i - 1] for i in range(1, len(data))]
        partsAudio = split_audio(data, sr, self.slice_ms, self.slice_ms, self.messages)
        needParts = []
        for i, part in enumerate(partsAudio):
            length = len([elem for elem in part if (np.absolute(elem - mu) / sigma) > 4])
            if length >= len(part) // 2:
                needParts.append(part)
                self.intervals_voices.append([i * self.slice_ms, (i + 1) * self.slice_ms])
            else:
                self.intervals_silence.append([i * self.slice_ms, (i + 1) * self.slice_ms])
        self.messages.insert(END, "Интервалы голоса образованы\n")
        self.name_voices_audio = "voices.wav"
        librosa.output.write_wav(path=self.path_audio + self.name_voices_audio,
                                 y=np.array(needParts).flatten(),
                                 sr=self.SR)
        self.intervals_silence = self.getIntervals(intervals=self.intervals_silence)
        self.intervals_voices = self.getIntervals(intervals=self.intervals_voices)

    def getIntervals(self, intervals):
        new_interval = True
        new_intervals = []
        for interval in intervals:
            if new_interval:
                new_intervals.append(interval)
                new_interval = False
            else:
                if interval[0] - new_intervals[len(new_intervals) - 1][1] > self.slice_ms:
                    new_intervals.append(interval)
                else:
                    new_intervals[len(new_intervals) - 1][1] = interval[1]
        return new_intervals

import os
import math
import librosa
import numpy as np
import moviepy.editor as mp
from scipy.signal import butter, lfilter
# from RESULT.training_gender import GenderClassificatory
from RESULT.training_human import HumanClassificatory


class Audio_Processing:
    SR = 16000
    slice_ms = 500
    area = 3

    def __init__(self, path_video, name_video, label):
        print(path_video + name_video)
        self.label = label
        self.nameVideo = name_video
        self.pathVideo = path_video
        self.to_extract_audio_from_video()
        self.filtering_audio()
        self.filteredPartsData = self.ExtractVoices(self.filtered_data_audio, self.SR)

    def to_extract_audio_from_video(self):
        self.label["text"] = "Извлекается аудио из видео..."
        # files = os.listdir(self.pathVideo)
        # video_file_clip = mp.VideoFileClip(self.pathVideo + files[0])
        video_file_clip = mp.VideoFileClip(self.pathVideo + self.nameVideo)
        audio_clip = video_file_clip.audio
        path_audio = self.pathVideo + "Audio/"
        os.makedirs(path_audio)
        name_original_audio = "Audio" + self.nameVideo
        audio_clip.write_audiofile(path_audio + name_original_audio, ffmpeg_params=["-ac", "1"])
        self.path_audio = path_audio
        self.name_original_audio = name_original_audio

    def filtering_audio(self):
        data_audio, sr = librosa.load(self.path_audio + self.name_original_audio, sr=self.SR)  # mono=False
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
            filtered_part_data_audio = lfilter(b, a, part_data_audio)
            self.filtered_data_audio[from_part_audio:to_part_audio] = filtered_part_data_audio
        self.nameFilteredAudio = self.path_audio + "Filtered_" + self.name_original_audio
        librosa.output.write_wav(self.nameFilteredAudio, self.filtered_data_audio, sr=self.SR)

    def ExtractVoices(self, data, sr):
        stepWindow = int((sr / 1000) * 200)
        partData = data[0:stepWindow]
        mu = np.sum(partData) / stepWindow
        sigma = np.sqrt(np.sum([(partData[i] - mu) ** 2 for i in range(stepWindow)]) / stepWindow)
        data = [data[i] - 0.95 * data[i - 1] for i in range(1, len(data))]
        partsAudio = self.split_audio(data, sr, self.slice_ms, self.slice_ms)
        needParts = []
        for part in partsAudio:
            length = len([elem for elem in part if (np.absolute(elem - mu) / sigma) > 3])
            if length >= len(part) // 2:
                needParts.append(part)
        return np.array(needParts)

    def split_audio(self, data, sr, window_ms, margin_ms):
        print("SplitAudio...")
        partsAudio = []
        stepWindow = int((sr / 1000) * window_ms)
        stepMargin = int((sr / 1000) * margin_ms)
        for i in range(0, len(data), stepMargin):
            partAudio = np.array(data[i:i + stepWindow])
            if len(partAudio) == stepWindow:
                partsAudio.append(partAudio)
        return partsAudio

    def get_statistics(self, L):
        dictionary = {}
        for a in L:
            if dictionary.get(a) is None:
                dictionary[a] = 1
            else:
                dictionary[a] += 1
        return dictionary

    def extract_not_presenter(self, parts_audio):
        # parts_audio = self.split_audio(filtered_data_audio, self.SR, self.slice_ms, self.slice_ms)
        # gender_classificatory = GenderClassificatory(self.pathAudio)
        human_classificatory = HumanClassificatory(self.path_audio)
        first_classification = []
        for i, part in enumerate(parts_audio):
            # genderPart = genderClassificatory.classification(self.SR, part)
            human_part = human_classificatory.Classification(self.SR, part)
            if human_part == "presenter":
                first_classification.append("presenter")
            else:
                first_classification.append("not_presenter")

        for i in range(len(first_classification)):
            left = first_classification[i - self.area: i]
            right = first_classification[i: i + self.area]
            stat_left = self.get_statistics(left)
            stat_right = self.get_statistics(right)
            if len(stat_left) > 1 and len(stat_right) > 1:
                stat = stat_right.copy()
                for e in stat.keys():
                    stat[e] = stat_left.get(e)
                max_value = np.max(list(stat.values()))
                new_human = [e for e in stat.keys() if stat.get(e) == max_value][0]
                first_classification[i] = new_human
        indexes = [i for i in range(len(first_classification)) if first_classification[i] == "not_presenter"]
        intervals = []
        new_interval = True
        for i in range(len(indexes)-1):
            if new_interval:
                interval = [indexes[i]*self.slice_ms]
                if indexes[i+1] - indexes[i] > 1:
                    interval.append((indexes[i]+1)*self.slice_ms)
                    intervals.append(interval)
                else:
                    new_interval = False
            elif (indexes[i+1] - indexes[i]) > 1:
                interval.append((indexes[i]+1)*self.slice_ms)
                intervals.append(interval)
                interval = []
                new_interval = True
        return intervals


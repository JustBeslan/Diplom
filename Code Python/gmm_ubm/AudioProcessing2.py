from tkinter import END
import numpy as np
from training_human import HumanClassificatory


class Audio_Processing2:

    def get_statistics(self, L):
        dictionary = {}
        for a in L:
            if dictionary.get(a) is None:
                dictionary[a] = 1
            else:
                dictionary[a] += 1
        return dictionary

    def extract_not_presenter(self, parts_audio):
        self.messages.insert(END, "Идет выделение голосов посторонних ведущему...\n")
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
        print(first_classification)
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
        self.messages.insert(END, "Интервалы времени выделены...\n")
        print(intervals)
        return intervals


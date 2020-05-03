from tkinter import END
import numpy as np


def getIntervalsPresenter(intervals_voices, intervals_not_presenter):
    intervals_presenter = []
    for interval_voice in intervals_voices:
        found_intervals = [interval_presenter for interval_presenter in intervals_not_presenter
                           if interval_presenter[0] >= interval_voice[0]
                           and interval_presenter[1] <= interval_voice[1]]
        if len(found_intervals) > 0:
            for i in range(len(found_intervals)):
                if i == 0 and interval_voice[0] < found_intervals[i][0]:
                    intervals_presenter.append([interval_voice[0], found_intervals[i][0]])
                if i == len(found_intervals) - 1 and found_intervals[i][1] < interval_voice[1]:
                    intervals_presenter.append([found_intervals[i][1], interval_voice[1]])
                if 0 < i <= len(found_intervals) - 1 and found_intervals[i - 1][1] < found_intervals[i][0]:
                    intervals_presenter.append([found_intervals[i - 1][1], found_intervals[i][0]])
        else:
            intervals_presenter.append(interval_voice)
    return intervals_presenter


def split_audio(data, sr, window_ms, margin_ms, messages):
    messages.insert(END, "Идет разделение аудио...\n")
    partsAudio = []
    stepWindow = int((sr / 1000) * window_ms)
    stepMargin = int((sr / 1000) * margin_ms)
    for i in range(0, len(data), stepMargin):
        partAudio = np.array(data[i:i + stepWindow])
        if len(partAudio) == stepWindow:
            partsAudio.append(partAudio)
    messages.insert(END, "Отдельные части аудио образованы\n")
    return partsAudio

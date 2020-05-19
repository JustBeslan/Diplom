import numpy as np


def correct2_intervals(intervalsA, intervalsB):
    result_intervalsB = []
    for intervalB in intervalsB:
        main_interval = []
        for intervalA in intervalsA:
            if intervalB[0] > intervalA[0] and intervalB[1] < intervalA[1]:
                main_interval = intervalA
                break
        if not main_interval:
            result_intervalsB.append(intervalB)
    return result_intervalsB


def correct_intervals(intervals, maxSilence):
    new_interval = True
    new_intervals = []
    for interval in intervals:
        if new_interval:
            new_intervals.append(interval)
            new_interval = False
        else:
            if interval[0] - new_intervals[len(new_intervals) - 1][1] > maxSilence:
                new_intervals.append(interval)
            else:
                new_intervals[len(new_intervals) - 1][1] = interval[1]
    return new_intervals


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


def split_audio(data, sr, window_ms, margin_ms):
    partsAudio = []
    stepWindow = int((sr / 1000) * window_ms)
    stepMargin = int((sr / 1000) * margin_ms)
    for i in range(0, len(data), stepMargin):
        partAudio = np.array(data[i:i + stepWindow])
        if len(partAudio) == stepWindow:
            partsAudio.append(partAudio)
    return partsAudio

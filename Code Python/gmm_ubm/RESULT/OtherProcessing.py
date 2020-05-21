import numpy as np

msec_in_hour = 3600000
msec_in_minute = 60000
msec_in_sec = 1000


def msToTime(interval):
    interval = np.array(interval)
    hours_interval = interval // msec_in_hour
    minutes_interval = (interval -
                        hours_interval * msec_in_hour) // msec_in_minute
    seconds_interval = (interval -
                        hours_interval * msec_in_hour -
                        minutes_interval * msec_in_minute) // msec_in_sec
    milliseconds_interval = (interval -
                             hours_interval * msec_in_hour -
                             minutes_interval * msec_in_minute -
                             seconds_interval * msec_in_sec)
    return hours_interval, minutes_interval, seconds_interval, milliseconds_interval


def timeToMS(time):
    return time.hour() * msec_in_hour + time.minute() * msec_in_minute + time.second() * msec_in_sec + time.msec()


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
    if len(intervals) > 0:
        new_intervals = [list(intervals[0]).copy()]
        s = 1
    else:
        new_intervals = []
        s = 0
    for i in range(s, len(intervals)):
        if abs(intervals[i][0] - new_intervals[len(new_intervals) - 1][1]) <= maxSilence:
            new_intervals[len(new_intervals) - 1][1] = intervals[i][1]
        else:
            new_intervals.append(list(intervals[i]).copy())
    return new_intervals


def extractOtherIntervals(intervalsA, intervalsB):
    otherIntervals = []
    for intervalA in intervalsA:
        foundSubIntervals = [intervalB for intervalB in intervalsB
                             if intervalB[0] >= intervalA[0] and intervalB[1] <= intervalA[1]]
        if len(foundSubIntervals) > 0:
            for i in range(len(foundSubIntervals)):
                if i == 0 and intervalA[0] < foundSubIntervals[i][0]:
                    otherIntervals.append([intervalA[0], foundSubIntervals[i][0]])
                if i == len(foundSubIntervals) - 1 and foundSubIntervals[i][1] < intervalA[1]:
                    otherIntervals.append([foundSubIntervals[i][1], intervalA[1]])
                if 0 < i <= len(foundSubIntervals) - 1 and foundSubIntervals[i - 1][1] < foundSubIntervals[i][0]:
                    otherIntervals.append([foundSubIntervals[i - 1][1], foundSubIntervals[i][0]])
        else:
            otherIntervals.append(intervalA)
    return otherIntervals


# print(extractOtherIntervals([[0, 1200], [1500, 1700]], [[100, 200], [576, 1034], [1500, 1560], [1560, 1600]]))
def split_interval(interval, len_split):
    intervals = []
    for i in range(abs(interval[1] - interval[0])//len_split):
        intervals.append([interval[0] + i * len_split, interval[0] + (i + 1) * len_split])
    return intervals

def split_audio(data, sr, window_ms, margin_ms):
    partsAudio = []
    stepWindow = int((sr / 1000) * window_ms)
    stepMargin = int((sr / 1000) * margin_ms)
    for i in range(0, len(data), stepMargin):
        partAudio = np.array(data[i:i + stepWindow])
        if len(partAudio) == stepWindow:
            partsAudio.append(partAudio)
    return partsAudio

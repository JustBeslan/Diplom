import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import fftpack


def SplitAudio(data, sr, window_ms, margin_ms):
    print("SplitAudio...")
    partsAudio = []
    stepWindow = int((sr / 1000) * window_ms)
    stepMargin = int((sr / 1000) * margin_ms)
    # count_step = math.ceil(len(data) / stepMargin)
    for i in range(0, len(data), stepMargin):
        partAudio = np.array(data[i:i + stepWindow])
        if len(partAudio) == stepWindow:
            partsAudio.append(partAudio)
    return partsAudio


def getCharact(data, mu, sigma):
    p = [e for e in data if np.abs(e - mu) / sigma > 4]
    return len(p) >= len(data) // 2


path = "C:/Users/Ibrag/Desktop/Diplom/Test5/Audio/"
name = "Audiotest5.wav"
data, sr = librosa.load(path + name)

window = 200
margin = 200
parts = SplitAudio(data, sr, window, margin)

r = []
count = 0
i = 0

part = data[0:int(sr*(200/1000))]
mu = np.sum(part) / len(part)
sigma = np.sqrt(np.sum([(e - mu) ** 2 for e in part]) / len(part))
for part in parts:
    if getCharact(part, mu, sigma):
        r.append(part)
        count += 1
    elif count > 0 and count >= 10:
        print(i)
        librosa.output.write_wav(path + "parts/part_" + str(i) + ".wav",
                                 np.array(r).flatten(), sr)
        i += 1
        count = 0
        r = []
    else:
        r.append(part)

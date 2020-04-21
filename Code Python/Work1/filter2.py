import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter


def audioFilterNoiseButterFilter(path, name, lowcut=300, highcut=3000):
    sound_track = wave.open(path + name, 'r')

    nframes = sound_track.getnframes()
    framerate = sound_track.getframerate()
    T = nframes / framerate

    t = np.linspace(0, T, nframes, endpoint=False)
    sound_track.close()

    fs, data = wavfile.read(path + name)
    new_data = []

    for i in range(len(data)):
        new_data.append(data[i][0])

    new_data = np.array(new_data, dtype="float32")

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(6, [low, high], btype='band')

    filtered_data = lfilter(b, a, new_data)

    filtered_data = np.array(filtered_data, dtype="int16")
    wavfile.write(path + "filtered_" + name, fs, filtered_data)


audioFilterNoiseButterFilter("/home/beslan/Diplom/WorkWithVideo/Audio/", "It_trailer_Audio.wav")

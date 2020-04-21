from scipy.io import wavfile
import librosa
import numpy as np


def decomposition_wav(path, name, time_ms, confluence_coefficient):
    time_s = time_ms / 1000
    # fs, data = wavfile.read(path + name)
    data, fs = librosa.load(path + name)
    # print(fs)
    # print(len(data))
    # print(data)

    time_s_in_samples = float(fs) * time_s
    mfcc_characterisits = []
    i = 0
    while i < len(data):
        part_data = data[i: i + int(time_s_in_samples)]
        mfcc_characterisits_part_data = librosa.feature.mfcc(part_data, sr=fs)
        mfcc_characterisits.append(mfcc_characterisits_part_data)
        # wavfile.write(path + str(i//fs) + "-" + str(int(i + time_s_in_samples)//fs) + "_sec_" + name, fs, part_data)
        if i + int(time_s_in_samples) > len(data):
            break
        else:
            i += int(time_s_in_samples * confluence_coefficient)
    print(len(mfcc_characterisits))
    print(len(mfcc_characterisits[0]))
    print(len(mfcc_characterisits[0][0]))
    print(mfcc_characterisits[0][0][0])


decomposition_wav("C:\\Users\\Ibrag\\Desktop\\Diplom\\Wave_work\\", "filtered_3.wav", 500, 0.5)

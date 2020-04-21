import wave
import librosa.display
import matplotlib.pyplot as plt
import sklearn

song = wave.open(r"C:\Users\Ibrag\Desktop\Diplom\3.wav", "rb")
print(song.getparams())

x, sr = librosa.load(r"C:\Users\Ibrag\Desktop\Diplom\3.wav")
print(type(x), type(sr))

plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr)
plt.show()

X = librosa.stft(x)

Xdb = librosa.amplitude_to_db(abs(X))
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
plt.colorbar()

n0 = 9000
n1 = 39100
x1 = x[n0:n1]
plt.figure(figsize=(14, 5))
plt.plot(x1)
plt.grid()
zero_crossing = librosa.zero_crossings(x1, pad=False)
print(sum(zero_crossing))

spectral_centroids = librosa.feature.spectral_centroid(x1, sr=sr)[0]
# spectral_centroids.shape
# var = (775,)
frames = range(len(spectral_centroids))
t = librosa.frames_to_time(frames)


def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)


librosa.display.waveplot(x1, sr=sr, alpha=0.9)
plt.plot(t, normalize(spectral_centroids), color='r')

spectral_rolloff = librosa.feature.spectral_rolloff(x1+0.01, sr=sr)[0]
librosa.display.waveplot(x1, sr=sr, alpha=0.4)
plt.plot(t, normalize(spectral_rolloff), color='g')

mfccs = librosa.feature.mfcc(x1, sr=sr)
# Отображение
librosa.display.specshow(mfccs, sr=sr, x_axis='time')

mfccs = mfccs.astype(float)
mfccs = sklearn.preprocessing.scale(mfccs, axis=1)
print(len(mfccs))
print(mfccs.mean(axis=1))
print(mfccs.var(axis=1))
# librosa.display.specshow(mfccs, sr=sr, x_axis='time')

hop_length = 512
chromagram = librosa.feature.chroma_stft(x1, sr=sr, hop_length=hop_length)
plt.figure(figsize=(15, 5))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')

plt.show()

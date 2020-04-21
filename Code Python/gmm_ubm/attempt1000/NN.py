import numpy as np
import librosa


class neuron:
    def __init__(self, countInputNeurons):
        coeffic = 1 / np.sqrt(countInputNeurons)
        self.weights = np.random.uniform(0.5 - coeffic, 0.5 + coeffic, countInputNeurons)

    def distance(self, x):
        return np.sqrt(np.sum((x - self.weights) ** 2))

    def update_weights(self, x, learning_rate):
        self.weights = [self.weights[i] + learning_rate * (x[i] - self.weights[i]) for i in range(len(self.weights))]


class NN:
    def __init__(self, countInputNeurons, countClusters, learning_rate):
        self.learning_rate = learning_rate
        self.neurons = [neuron(countInputNeurons) for i in range(countClusters)]

    def train(self, X, countEpochs):
        for epoch in range(countEpochs):
            print("epoch : ", epoch)
            indexes = list(np.arange(len(X)))
            while len(indexes) != 0:
                rand_index = np.random.choice(indexes)
                x = X[rand_index]
                indexes.remove(rand_index)
                distances = [neuron.distance(x) for neuron in self.neurons]
                winner_neuron = self.neurons[int(np.argmin(distances))]
                winner_neuron.update_weights(x, self.learning_rate)
            self.learning_rate = self.learning_rate - 0.05

    def test(self, x):
        distances = [neuron.distance(x) for neuron in self.neurons]
        return np.argmin(distances)


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


def toMel(f):
    return 1127 * np.log(1 + f / 700)


def toBark(f):
    return 8.96 * np.log(0.978 + 5 * np.log(0.994 + pow((f + 75.4) / 2173, 1.347)))


def getFeature(data):
    mfcc = np.array(librosa.feature.mfcc(data, sr, n_mfcc=12)).flatten()
    freqs = np.abs(np.fft.fft(data))**2
    mels = [toMel(f) for f in freqs]
    mel = (np.max(mels) + np.min(mels))/2
    res = np.append([], mfcc)
    return res


path = "C:/Users/Ibrag/Desktop/Diplom/Test5/Audio/"
name = "FilteredAudiotest5.wav"
data, sr = librosa.load(path + name)
parts = SplitAudio(data, sr, 30, 30)
features = []
for part in parts:
    # print(getFeature(part).shape)
    features.append(getFeature(part))


print(np.array(features).shape)
nn = NN(np.array(features).shape[1], 2, 0.6)
nn.train(features, 1000)

for part in parts:
    print(nn.test(getFeature(part)))


from struct import *
import matplotlib.pyplot as plt
import cmath


def read_file(path, name):
    f = open(path + name, "rb")
    raw_input = []
    chunk = f.read(2)
    while chunk:
        raw_input.append(unpack('<h', chunk)[0])
        chunk = f.read(2)
    f.close()
    return raw_input

def dft(fnList):
    pi2 = cmath.pi*2.0
    N = len(fnList)
    FmList = []
    for m in range(N):
        Fm = 0.0
        for n in range(N):
            Fm += fnList[n] * cmath.exp(-1j * pi2 * m * n / N)
        FmList.append(abs(Fm / N))
    return FmList


path = "C:/Users/Ibrag/Desktop/Diplom/Videos/Test3/Audio/"
name = "voices.wav"
raw_input = read_file(path, name)
spectrum = dft(raw_input)
plt.plot(spectrum[0:400], 'r')
plt.show()



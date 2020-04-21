import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import math

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
#    print(x)
#    print(progress)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
#    print(hours,mins,secs)
    out = "0:%02d:%02d" % (mins, secs)
    if hours > 0:
#        out = "%d:" % hours
        out = "%d:%02d:%02d" % (hours, mins, secs)
#    print(out)
    return out

def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    print(peak)
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)

def time_file(dur):
    hour = dur // 3600
    print(hour)
    dur -= 3600*hour
    minutes = dur // 60
    print(minutes)
    dur -= 60*minutes
    print(dur)

wav = wave.open("/home/beslan/audio.wav", mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

duration = nframes / framerate
print(duration)
time_file(duration)
w, h = 800, 300
k = nframes/w/32
DPI = 72
peak = 256 ** sampwidth / 2

content = wav.readframes(nframes)
samples = np.fromstring(content, dtype=types[sampwidth])

plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
plt.subplots_adjust(wspace=0, hspace=0)


for n in range(nchannels):
    channel = samples[n::nchannels]

    channel = channel[0::int(k)]

    if nchannels == 1:
        channel = channel - peak
    if n == 1:
        axes = plt.subplot(1, 1, 1)
        axes.plot(channel, "g")

#    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
plt.grid(True, color="w")
#    plt.axvline(x=1)
#    axes.xaxis.set_major_formatter(ticker.NullFormatter())
for i in range(len(channel)):
    print(channel[i])
#axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.axvline(x=2 / (duration * k) *float(nframes))
print(2 / (duration * k) *float(nframes))
plt.savefig("wave", dpi=DPI)
plt.show()
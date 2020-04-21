import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime as dt

fmt = dates.DateFormatter('%H:%M:%S')

fig, ax = plt.subplots()

time_interval = ['0:0:0', '0:1:0', '0:2:0', '0:3:0', '1:52:42']
time_interval = [dt.datetime.strptime(i, "%H:%M:%S") for i in time_interval]
y = np.random.randn(5)
x = np.array([x for x in range(5)])
ax.plot(time_interval, y, "-o")
ax.xaxis.set_major_formatter(fmt)
fig.autofmt_xdate()
plt.show()
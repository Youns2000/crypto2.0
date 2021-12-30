import matplotlib.pyplot as plt
import numpy as np
import datetime, csv
import os

def add_time(ms_time, h, m, s):
    return ms_time + h * 60 * 60 * 1000 + m * 60 * 1000 + s * 1000

def milli_convert(millis):
    dt = datetime.datetime.fromtimestamp(millis / 1000.0, tz=datetime.timezone.utc)
    return dt

def save_graph(data, name):
    x, y = [], []

    for t in data['time']:
        x.append(float(t))
    for v in data['values']:
        y.append(float(v))

    plt.plot(x, y)
    plt.title(name)
    plt.xlabel("TIME")
    plt.ylabel("VALUES")
    if (os.path.isdir('graphs') == False):
            os.mkdir('graphs')
    plt.show()
    # plt.savefig('graphs/'+name+'.png', transparent=False)

def average_graph(data):
    t_v = {}
    for d in data:
        arr = np.array(d[2:4])
        arr = arr.astype(np.float)
        t_v[d[0]] = np.average(arr)
    return t_v

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string
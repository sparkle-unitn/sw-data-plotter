#!/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt


# get next line, ignoring comments (with # syntax) and empty lines
def input_next_line():
    while True:
        s = input().split('#')[0].strip()
        if len(s):
            return s

# from a string containing whitespace-separated numbers return an array of floats. * in the string will correspond to a None value in the array
def str_to_array_of_optional_floats(s):
    ret = []
    for word in s.split():
        if word == "*":
            ret.append(None)
        else:
            ret.append(float(word))
    return ret



#read from the path specified in the first command line arg
if len(sys.argv) > 1:
    sys.stdin = open(sys.argv[1], 'r')
else:
    print("usage: %s INPUT_FILE" % sys.argv[0])
    exit(1)


# get number of signals
number_of_signals = int(input_next_line())

# each signal is a tuple of two parallel arrays and a label. 1st element is x values, 2nd y values, third label
signals = []

# get each signal's data
for _ in range(number_of_signals):
    # get signal label
    label = input_next_line()
    # get number of samples
    samples = int(input_next_line())
    # get samples
    x = np.array([])
    y = np.array([])
    for _ in range(samples):
        sample = str_to_array_of_optional_floats(input_next_line())
        x = np.append(x, sample[0])
        y = np.append(y, sample[1])
    signals.append((x,y,label))


print("signals: ")
for x,y,label in signals:
    print("%s: %d datapoints" % (label,len(y)))

# interpolate missing x-coord values
for x,_,_ in signals:
    for i in range(len(x)):
        #make a dictionary with the contents of x
        x_dict = {i:v for i,v in enumerate(x) if v != None }

        x[i] = np.interp(i, [*x_dict.keys()], [*x_dict.values()])


# actually plot the signal
for x,y,label in signals:
    plt.plot(x, y, ".", label=label)
plt.legend(loc="upper left")
plt.show()


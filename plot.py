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


# get number of samples and signals
samples = int(input_next_line())
number_of_signals = int(input_next_line())

# each signal is a pair of parallel arrays. the first is for the x values, the second for the y values
signals = [(np.array([]), np.array([]))] * number_of_signals

# get signal data
for i in range(samples):
    sample = str_to_array_of_optional_floats(input_next_line())
    for j in range(number_of_signals):
        x, y = signals[j]
        x = np.append(x, sample[j*2])
        y = np.append(y, sample[j*2+1])
        signals[j] = (x, y)

# interpolate missing x-coord values
for x,_ in signals:
    for i in range(len(x)):
        #make a dictionary with the contents of x
        x_dict = {i:v for i,v in enumerate(x) if v != None }

        x[i] = np.interp(i, [*x_dict.keys()], [*x_dict.values()])


# actually plot the signal
for x,y in signals:
    plt.plot(x, y)
plt.show()


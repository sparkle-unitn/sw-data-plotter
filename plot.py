#!/bin/python3

import sys
import math
import numpy as np
import matplotlib.pyplot as plt



def main():
    #read from the path specified in the first command line arg
    if len(sys.argv) > 1:
        input_file = open(sys.argv[1], 'r')
    else:
        print("usage: %s INPUT_FILE" % sys.argv[0])
        exit(1)
    
    
    signals = get_signals_data(input_file)
    
    interpolate_x_values(signals)

    print("%s" % [signals])
    
    print_signals_info(signals)
    
    plot_signals(signals)

# get next line, ignoring comments (with # syntax) and empty lines. returns None on EOF
def input_next_line(fp):
    while True:
        s = fp.readline()
        if s == '':
            return None # EOF reached
        s = s.split('#')[0].strip()
        if len(s):
            return s

def get_signal_len(fp):
    old_pos = fp.tell()
    ret = 0
    while True:
        l = input_next_line(fp)
        if l == "END_OF_SIGNAL":
            fp.seek(old_pos)
            return ret
        ret += 1

# from a string containing whitespace-separated numbers return an array of floats. * in the string will correspond to a None value in the array
def str_to_array_of_optional_floats(s):
    ret = []
    for word in s.split():
        if word == "*":
            ret.append(float('nan'))
        else:
            ret.append(float(word))
    return ret


# read the input file, returns an dictionary of signals, where each signal is a tuple of two parallel arrays with its label as key {label : (x_array, y_array), ...}
def get_signals_data(fp):
    signals = {}

    # get each signal's data
    while True:
        # get signal label
        label = input_next_line(fp)
        if label == None:
            break # EOF

        signal_len = get_signal_len(fp)
        x = np.empty(signal_len)
        y = np.empty(signal_len)

        # get samples
        for i in range(signal_len):
            line = input_next_line(fp)
            if line == "END_OF_SIGNAL":
                break
            sample = str_to_array_of_optional_floats(line)
            x[i] = sample[0]
            y[i] = sample[1]
        else:
            assert(input_next_line(fp) == "END_OF_SIGNAL")

        signals[label] = (x,y)
    return signals


# interpolate missing x-coord values
def interpolate_x_values(signals):
    for label in signals:
        x,_ = signals[label]
        for i in range(len(x)):
            if math.isnan(x[i]):
                #make a dictionary with the contents of x
                x_dict = { i:v for i,v in enumerate(x) if not math.isnan(v) }
        
                x[i] = np.interp(i, [*x_dict.keys()], [*x_dict.values()])

# print signal information: how many datapoints, deltax from beginning to end, sample frequency
def print_signals_info(signals):
    print("signals: ")
    for label,(x,y) in signals.items():
        deltax = max(x) - min(x)
        print("\t%s: %d datapoints / %f delta x = %f" % (label, len(y), deltax, len(y)/deltax))

# plot the signals with matplotlib
def plot_signals(signals):
    def expand(x,y, gap=1e-4):
        add = np.tile([0, gap, np.nan], len(x))
        x1 = np.repeat(x, 3) + add
        y1 = np.repeat(y, 3) + add
        return x1, y1
    plt.rcParams['lines.solid_capstyle'] = 'round'
    
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, title="Test scatter")
    for label, (x,y) in signals.items():
        ax.plot(*expand(x,y), label=label, lw=4, alpha=0.7)
    
    plt.legend(loc="upper left")
    plt.show()



main()

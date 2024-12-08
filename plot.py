#!/bin/python3

import sys
import math
import argparse
import numpy as np

import time

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser()

    default_maximum = 4096
    default_backend = 'matplotlib'

    parser.add_argument('filename', type=str, help='Path to data file')
    parser.add_argument('--line-mode', action='store_true', help='A boolean switch that controls whether the program is in line mode or in scatter mode')
    parser.add_argument('--maximum', type=int, default=default_maximum, help='Maximum value for the signals, after which they get clipped (default: '+str(default_maximum)+')')
    parser.add_argument('--backend', default=default_backend, choices=['matplotlib', 'bokeh'], help='Sets the rendering backend (default: '+default_backend+')')

    args = parser.parse_args()

    input_file = open(args.filename, 'r')

    signals = get_signals_data(input_file, args.maximum)

    interpolate_x_values(signals)

    print_signals_info(signals)

    plot_signals(signals, args.line_mode, args.backend)

    end_time = time.time()
    print("finished in " + str(end_time - start_time) + " seconds")

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

# from a string containing whitespace-separated numbers return an array of floats. * in the string will correspond to a NaN value in the array
def str_to_array_of_optional_floats(s):
    ret = []
    for word in s.split():
        if word == "*":
            ret.append(float('nan'))
        else:
            ret.append(float(word))
    return ret

# read the input file, returns an dictionary of signals, where each signal is a tuple of two parallel arrays with its label as key {label : (x_array, y_array), ...}
def get_signals_data(fp, maximum):
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
            try:
                sample = str_to_array_of_optional_floats(line)
            except:
                print("warning: line '" + line + "' could not be converted to array of optional floats")
                continue

            if len(sample) < 2:
                print("warning: line '" + line + "' should contain 2 values")
                continue
            x[i] = sample[0]
            y[i] = min(sample[1], maximum)
        else:
            assert(input_next_line(fp) == "END_OF_SIGNAL")

        # if the label already exists only concatenate the new points, otherwise create a new signal
        if label in signals:
            signals[label] = (
                np.concatenate((signals[label][0], x)),
                np.concatenate((signals[label][1], y))
            )
        else:
            signals[label] = (x,y)
    return signals

# interpolate missing x-coord values
def interpolate_x_values(signals):
    for label in signals:
        x,_ = signals[label]
        x_dict = None
        for i in range(len(x)):
            if math.isnan(x[i]):
                if x_dict == None:
                    #make a dictionary with the contents of x
                    x_dict = { i:v for i,v in enumerate(x) if not math.isnan(v) }

                x[i] = np.interp(i, [*x_dict.keys()], [*x_dict.values()])


# print signal information: how many datapoints, deltax from beginning to end, sample frequency
def print_signals_info(signals):
    print("signals:")
    for label,(x,y) in signals.items():
        deltax = max(x) - min(x)
        print("> %s: %d datapoints / %f delta x = %f" % (label, len(y), deltax, len(y)/deltax))


# plot the signals with the chosen backend
def plot_signals(signals, line_mode, backend):
    if backend == "matplotlib":
        import matplotlib as mpl
        from matplotlib import pyplot as plt
        from mplcairo import operator_t # mpl backend for additive blending support

        # set mplcairo as mpl backend
        mpl.use("module://mplcairo.qt")
        # supposedly increases performance
        mpl.style.use("fast")
        mpl.rcParams['path.simplify_threshold'] = 1.0


        fig, ax = plt.subplots()
        # The figure and axes background must be made transparent to use additive blending
        fig.patch.set(alpha=0, color="#000000")
        ax.patch.set(alpha=0, color="#000000")

        color_palette = ['#ff0000', '#0000ff', '#00ff00', 'c', 'm', 'y', 'k']

        for i, (label, (x,y)) in enumerate(signals.items()):
            color = color_palette[i % len(color_palette)]

            if line_mode:
                ax.plot(x,y,c=color,label=label,marker='.')
            else:
                pc = ax.scatter(x, y, c=color, label=label, marker='.')
                operator_t.ADD.patch_artist(pc)  # Use additive blending.

        plt.legend(loc="upper left")
        plt.show()
    elif backend == "bokeh":
        from bokeh.plotting import figure, show

        p = figure(title="Plot", x_axis_label='x', y_axis_label='y', output_backend="webgl")
        p.sizing_mode = "stretch_both"
        color_palette = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'black']
        # add a line renderer with legend and line thickness to the plot
        for i, (label,(x,y)) in enumerate(signals.items()):
            color = color_palette[i%len(color_palette)]
            if line_mode:
                p.line(x, y, legend_label=label, line_width=2, line_color=color)
            else:
                p.scatter(x, y, legend_label=label, size=2, color=color)

        # show the results
        show(p)

main()

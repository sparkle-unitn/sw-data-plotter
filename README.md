# Data Plotter

Data Plotter is a simple tool useful to plot data, specifically streams of data sent by a microcontroller. 

Data needs to be written on a file that is then passed as argument to the program, which will parse the file and display a graph.

## Dependencies

The script depends on `numpy`, `matplotlib` and `mplcairo`

## Usage

`python plot.py INPUT_FILE [line]`

where `INPUT_FILE` is the path to a text file with the following structure:

- Each signal is represented by a series of lines with the following structure:
    1. a line containing the label for the signal, to be displayed in the legend;
    1. a line for each sample, containing a whitespace-separated pair of coordinates to plot;
        * some x values may be omitted by specifying `*` instead, and they will be interpolated between adjacent ones. This feature is meant to be used with values obtained through DMA, which are harder to put a timestamp on.
            * Interpolation of the first/last value(s) is impossible, and will yield the x of the next/previous point;
            * to ensure correct interpolation x values must be monotonically nondecreasing.

The word 'line', specified after the input file, changes the visualization from a scatter plot to a line plot

Comments and spacing:
* if an input line contains '#' followed by any other characters those will be considered a comment and ignored ('#' included, of course);
* empty lines and lines containing only whitespace or comments will be ignored;
* whitespace at the beginning and end of input lines will be ignored.

## Example input file

```
1 # number of signals

name of signal # the name that will appear in the graph's legend
3 # number of samples
# list of "x y" tuples to plot. x should always increase
1 2
2 3
3 8 
```

Some other more advanced example input files are provided under `example_inputs/`.


## Profiling:
You may profile the script with the following command:

```
python -m pyflame -a "--width 4000" plot.py example_inputs/many_points.txt
```

> [!NOTE]
> Before running it pyflame and flamegraph need to be installed.

The command will generate a file "plot.py.svg" in the working directory. To visualize it you may use gimp or any other image viewer supporting svg.


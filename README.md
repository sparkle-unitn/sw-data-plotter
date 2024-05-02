# Data Plotter

Data Plotter is a simple tool useful to plot data, specifically streams of data sent by a microcontroller. 

Data needs to be written on a file that is then passed as argument to the program, which will parse the file and display a graph.

## Usage

`python plot.py INPUT_FILE`

where `INPUT_FILE` is the path to a text file with the following structure:

1. on the first line the number of samples collected;
1. on the second line the number of separate signals to be displayed;
1. the rest of the lines will contain the actual signal data. each line will represent a single sample, and is formed by whitespace separated numbers read in pairs. each pair will represent the x (generally the acquisition time) and y (generally the value being read) values.
    * the x values must always be ordered
    * some x values can be omitted by specifying '\*' instead, and they will be interpolated between other existing readings (which is why it is needed for them to be in order). Interpolation of the first or last values is impossible and will not yield useful results, but the rest of the graph will still be displayed. (This feature is meant to be used with values obtained through DMA, which are harder to put a timestamp on)

Comments:
* if an input line contains '#' followed by any other characters those will be considered a comment ('#' included obviously)
* empty lines and lines containing only whitespace or comments will be ignored

## Example input file

```
3 # number of samples
1 # number of signals

# list of "x y" tuples to plot
1 2
2 3
3 8
```

some other more advanced example input files are provided under example_inputs/

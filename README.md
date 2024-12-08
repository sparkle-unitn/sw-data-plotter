# Data Plotter

Data Plotter is a simple tool useful to plot data, specifically streams of data sent by a microcontroller.

Data needs to be written on a file that is then passed as argument to the program, which will parse the file and display a graph.

## Dependencies

The script depends on `numpy`, and other packages depending on the chosen backend:
- for the matplotlib backend: `matplotlib`, `mplcairo` and `pyqt5` (or `pyqt6`)
- for the bokeh backend: `bokeh`

The user may use the provided `requirements.txt` file to install all dependencies (and backend dependencies) by running
```bash
pip install -r requirements.txt
```

## Usage
```
usage: plot.py [-h] [--line-mode] [--maximum MAXIMUM] [--backend {matplotlib,bokeh}] filename

positional arguments:
  filename              Path to data file

options:
  -h, --help            show this help message and exit
  --line-mode           A boolean switch that controls whether the program is in line mode or in
                        scatter mode
  --maximum MAXIMUM     Maximum value for the signals, after which they get clipped (default: 4096)
  --backend {matplotlib,bokeh}
                        Sets the rendering backend (default: matplotlib)

```
where `filename` is the path to a text file with the following structure:

- Each signal is represented by a series of lines with the following structure:
    1. a line containing the label for the signal, to be displayed in the legend;
    1. a line for each sample, containing a whitespace-separated pair of coordinates to plot;
        * some x values may be omitted by specifying `*` instead, and they will be interpolated between adjacent ones. This feature is meant to be used with values obtained through DMA, which are harder to put a timestamp on.
            * Interpolation of the first/last value(s) is impossible, and will yield the x of the next/previous point;
            * to ensure correct interpolation x values must be monotonically nondecreasing.
        * if a sample line does not respect this syntax the script will try to ignore it, outputting a warning. this is useful for unreliable channels of communication where it is not crucial to never lose any samples;
    1. a line contanining the string "END_OF_SIGNAL"
- The file may contain more than one signal block with the same signal label; in that case the points will be added to the same label, allowing interleaving signals.

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
END_OF_SIGNAL
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


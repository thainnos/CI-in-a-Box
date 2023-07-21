#!/usr/bin/python3

import itertools
import numpy as np
from bokeh.models import Legend
from bokeh.palettes import Dark2_5
from bokeh.resources import INLINE
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.models import NumeralTickFormatter

output_notebook(INLINE, hide_banner=True)

trace_array = np.load('../chipwhisperer-pre/example_traces/' +
                      '250_traces/trace_array.npy')
# '500_traces/trace_array.npy')
# '2500_traces/trace_array.npy')
plots = np.load('../analyze/results/global_plots.npy')
key_guesses = np.load('../analyze/results/key_guesses.npy')

num_points = np.shape(trace_array)[1]  # samples per trace

p = figure()

p.plot_width = 975
p.yaxis[0].formatter = NumeralTickFormatter(format="0.0000")
colors = itertools.cycle(Dark2_5[:len(plots)])

legend1_items, legend2_items = [], []
for i, (plot, guess, color) in enumerate(zip(plots, key_guesses, colors)):
    line = p.line(x=range(num_points), y=plot, color=color)
    line.visible = True if i == 0 else False
    legend_item = (str(i) + ': ' + str(hex(int(guess))), [line])
    if i <= len(plots) / 2:
        legend1_items.append(legend_item),
    else:
        legend2_items.append(legend_item),

legend1 = Legend(items=legend1_items,
                 location=(7, 2),
                 spacing=10,
                 label_width=10,
                 label_text_font_style='bold',
                 orientation="horizontal")

legend2 = Legend(items=legend2_items,
                 location=(7, 2),
                 spacing=10,
                 label_width=10,
                 label_text_font_style='bold',
                 orientation="horizontal")

p.add_layout(legend1, 'below')
p.add_layout(legend2, 'below')

p.legend.click_policy = "hide"

show(p)

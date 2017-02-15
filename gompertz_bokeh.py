#!/usr/bin/env python
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.plotting import figure, output_file, show
import numpy as np

output_file("www/gompertz.html")

def gompertz(a, b, c, t):
    return a*np.exp(-b*np.exp(-c*t))

a_start = 1
b_start = 6
c_start = 0.14

x = np.arange(0, 50, 0.1)
y = gompertz(a_start, b_start, c_start, x) 

source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(plot_width=400, plot_height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

sliders = {
    'a': Slider(start=1, end=1000000, value=a_start, step=1000, title="a"),
    'b': Slider(start=0, end=50, value=b_start, step=0.5, title="b"),
    'c': Slider(start=0, end=1, value=c_start, step=.01, title="c"),
}

callback = CustomJS(
    args=dict(source=source, **sliders), 
    code="""
        var data = source.data;
        x = data['x']
        y = data['y']
        for (i = 0; i < x.length; i++) {
            y[i] = a.value * Math.exp(-b.value * Math.exp(-c.value*x[i]))
        }
        source.trigger('change');
    """)


for slider in sliders.values():
    slider.js_on_change('value', callback)

layout = column(sliders['a'], sliders['b'], sliders['c'], plot)

show(layout)

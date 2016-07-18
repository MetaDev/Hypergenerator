# -*- coding: utf-8 -*-

import sys
import numpy as np


# p12-a: Hexagonal Gosper Curve
#n = 4
#delta = 60.0
#axiom = "F"
#productions = {'F': 'F+f++f-F--FF-f+', 'f' : '-F+ff++f+F--F-f'}

# put rules in dictionary, of form name_rule, rule_string
# make a vocabulary with start and end symbols

stack = []
lines = []
# todo add string manipulation as possibility to turtle graphics


def copy(pos, angle, n):
    return (pos, angle, n)


def prod_f(pos, angle, n):
    pos1 = pos + np.array((d * np.cos(np.deg2rad(angle)),
                           d * np.sin(np.deg2rad(angle))))
    lines.append(pos)
    lines.append(pos1)
    return (pos1, angle, n)
productions = {
    "F": ("-F+ff++f+F--F-f", prod_f),
    "f": ("F+f++f-F--FF-f+", copy)
}
t = 60
angle = 90


def decode(string, pos, angle, n):
    for c in string:
        if c == '-':
            angle -= t
        elif c == '+':
            angle += t
        elif c == '[':
            stack.append((pos, angle, n))
        elif c == ']':
            (pos, angle, n) = stack.pop()
        elif n > 0:
            (pos, angle, n) = productions[c][1](pos, angle, n)
            decode(productions[c][0], *productions[c][1](pos, angle, n - 1))

d = 1
# bundle line calls-> Lin(connect='strip') add all coordinates to numpy array


def draw_line(pos, pos1, angle, width):
    scene.visuals.Line(pos=np.array((pos, pos1)),
                       color=(1, 1, 0, 1), parent=viewbox.scene)


def draw_ellips(pos, width):
    scene.visuals.Ellipse(center=pos, radius=width)


from vispy import app, scene, visuals

canvas = scene.SceneCanvas(keys='interactive', show=True)
grid = canvas.central_widget.add_grid(spacing=0)

viewbox = grid.add_view(row=0, col=1, camera='panzoom')

# add some axes
x_axis = scene.AxisWidget(orientation='bottom')
x_axis.stretch = (1, 0.1)
grid.add_widget(x_axis, row=1, col=1)
x_axis.link_view(viewbox)
y_axis = scene.AxisWidget(orientation='left')
y_axis.stretch = (0.1, 1)
grid.add_widget(y_axis, row=0, col=0)
y_axis.link_view(viewbox)
#
# expand grammar
n = 5               # max depth of recursion
decode("F", np.array((0, 0)), 90, n)

# draw lines
scene.visuals.Line(pos=np.array(lines), color=(1, 1, 0, 1),
                   connect='segments', parent=viewbox.scene)


def update(event):
    pass

timer = app.Timer('auto', connect=update, start=True)
viewbox.camera.set_range()


canvas.show()
if sys.flags.interactive == 0:
    app.run()

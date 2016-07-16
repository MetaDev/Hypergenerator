import sys
import numpy as np
from vispy import app, scene, visuals

canvas = scene.SceneCanvas(keys='interactive', show=True)
grid = canvas.central_widget.add_grid(spacing=0)

viewbox = grid.add_view(row=0, col=1, camera='panzoom')

lines = [scene.visuals.Line(pos=np.array(((-10,1),(50,100*i))), color=(1,1,0,1), parent=viewbox.scene)
                      for i in range(6)]

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

def update(event):
    for line in lines:
        scale = [np.sin(np.pi * event.elapsed)+2,
                 np.cos(np.pi * event.elapsed)+2]
        line.transform.scale = scale

timer = app.Timer('auto', connect=update, start=True)
viewbox.camera.set_range()


canvas.show()
if sys.flags.interactive == 0:
    app.run()


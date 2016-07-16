import numpy as np
from vispy.io import imread

img_data = imread('001.jpg')
width=len(img_data)
height=len(img_data[0])
line_number=1000
img_data=np.array(img_data)
print(width)
print(height)

for i in range(line_number):
    start=np.random.randint(0,width),np.random.randint(0,height)
    stop=np.random.randint(0,width),np.random.randint(0,height)
    start,stop=tuple(np.sort([start,stop],0))
    line = zip(np.linspace(start[0], stop[0], np.max(stop-start),endpoint=False),np.linspace(start[1], stop[1], np.max(stop-start),endpoint=False))
    #round coordinates
    line = np.round(list(line))
    #remove duplicates
    temp_line=[tuple(coord) for coord in line]

    line=[]
    seen = set()
    for coord in temp_line:
        if coord not in seen:
            seen.add(coord)
            line.append((int (coord[0]),int(coord[1])))
    pixels=np.array([img_data[coord[0]][coord[1]] for coord in line])
    #np.random.shuffle(pixels)


    for i,coord in enumerate(line):
        img_data[coord]=pixels[i]

from vispy import app, scene, visuals

canvas = scene.SceneCanvas(keys='interactive', show=True)
viewbox = canvas.central_widget.add_view()

interpolation = 'nearest'
image = scene.visuals.Image(img_data, interpolation=interpolation,
                            parent=viewbox.scene, method='subdivide')
viewbox.camera = scene.PanZoomCamera(aspect=1)
viewbox.camera.flip = (0, 1, 0)
viewbox.camera.set_range()
canvas.show()
app.run()

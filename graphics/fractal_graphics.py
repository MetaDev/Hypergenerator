import numpy as np


from matplotlib import pyplot as plt
from matplotlib import colors
dpi_resolution=320
dpi_view=320
#golden ration number
phi = (1 + 5 ** 0.5) / 2
#natural number
e=np.exp(0)
from vispy.io import imread


def mandelbrot_image(xmin,xmax,ymin,ymax,width=3,height=3,maxiter=80,cmap='hot',image=None):
    img_width = dpi_resolution * width
    img_height = dpi_resolution * height
    x,y,z,c = mandelbrot_set(xmin,xmax,ymin,ymax,img_width,img_height,maxiter,image)

    fig, ax = plt.subplots(figsize=(width, height),dpi=dpi_view)
    ticks = np.arange(0,img_width,3*dpi_resolution)
    x_ticks = xmin + (xmax-xmin)*ticks/img_width
    plt.xticks(ticks, x_ticks)
    y_ticks = ymin + (ymax-ymin)*ticks/img_width
    plt.yticks(ticks, y_ticks)

    #normalise seperately for each channel
    vmin, vmax = z.min(), z.max()
    z = (z-vmin)/(vmax-vmin)

    return z.T
from numba import jit



@jit
def mandelbrot(c,maxiter,pixel,image):
    z = c
    dz=0
    point = pixel[0]/255 + pixel[2]/255*1.0j
    dist = 1e5;
    # image[abs(int(z.real)),abs(int(z.imag))][0]
    for n in range(maxiter):
        if abs(z) > 40:
            return image[int(z.real)%400,int(z.imag)%400][1],1
        z= (1/(2*np.pi))* np.exp(-z/2) +c
        dist = min(dist, abs(z - image[int(z.real)%400,int(z.imag)%400][1]));
    return dist,0

@jit
def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter,image):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width,height))
    cs= np.empty((width,height))
    for i in range(width):
        for j in range(height):
           n3[i,j],cs[i,j] = mandelbrot(r1[i] + 1j*r2[j],maxiter,image[i,j],image)
    return (r1,r2,n3,cs)


img_data = imread('glitch2.png')
img_data=np.array(img_data)

img=mandelbrot_image(-20.0,20,-20,20,maxiter=320,cmap='gnuplot2',image=img_data)

from vispy import app, scene, visuals

canvas = scene.SceneCanvas(keys='interactive', show=True)
viewbox = canvas.central_widget.add_view()

interpolation = 'nearest'
image = scene.visuals.Image(img, cmap='cubehelix', interpolation=interpolation,
                            parent=viewbox.scene, method='subdivide')
viewbox.camera = scene.PanZoomCamera(aspect=1)
viewbox.camera.flip = (0, 1, 0)
viewbox.camera.set_range()
canvas.show()
app.run()



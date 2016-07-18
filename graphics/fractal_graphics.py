import numpy as np
from vispy.io import imread
from numba import jit
from vispy import app, scene, visuals


dpi_resolution = 320
dpi_view = 320
# golden ration number
phi = (1 + 5 ** 0.5) / 2
# natural number
e = np.exp(0)


def fractal_image(xmin, xmax, ymin, ymax, width=3, height=3, maxiter=80,
                  image=None):
    img_width = dpi_resolution * width
    img_height = dpi_resolution * height
    x, y, z, c = mandelbrot_set(
        xmin, xmax, ymin, ymax, img_width, img_height, maxiter, image)

    # normalise seperately for each channel
    vmin, vmax = z.min(), z.max()
    z = (z - vmin) / (vmax - vmin)

    return z.T

# possible parameters: a formula with both functions and boolean logic
# the excape condition (abs(z)>x)
# the colormapping, use distance based or number of iterations
# the current final colormapping comes from vispy, experiment with it
# combined with image, which can be either direct 1-1 pixel or use a value
# to derive the pixel value used from anywhere in the image


@jit
def fractal_pixel(c, maxiter, pixel, image):
    z = c
    dz = 0
    point = pixel[0] / 255 + pixel[2] / 255 * 1.0j
    dist = 1e5
    # image[abs(int(z.real)),abs(int(z.imag))][0]
    for n in range(maxiter):
        if abs(z) > 40:
            return image[int(z.real) % 400, int(z.imag) % 400][1], 1
        z = (1 / (2 * np.pi)) * np.exp(-z / 2) + c
        dist = min(
            dist, abs(z - image[int(z.real) % 400, int(z.imag) % 400][1]))
    return dist, 0


@jit
def fractal(xmin, xmax, ymin, ymax, width, height, maxiter, image):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    cs = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i, j], cs[i, j] = fractal_pixel(
                r1[i] + 1j * r2[j], maxiter, image[i, j], image)
    return (r1, r2, n3, cs)


img_data = imread('glitch2.png')
img_data = np.array(img_data)

img = fractal_image(-20.0, 20, -20, 20, maxiter=320,
                    cmap='gnuplot2', image=img_data)


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

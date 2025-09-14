"""
Visual tests for the class Shape
"""
from src.graphics.shape import Shape

"""
A simple script to check that OpenGL is working.
"""
import glfw
from OpenGL.GL import *
import numpy as np


#GLOBALS
#window width and height in pixels
width, height = 1000, 800


def window_resize(window, width, height):
    """
    Automatically adjust image to acount for window resizing by user.
    """
    glViewport(0,0,width, height)


if not glfw.init():
    raise Exception("GLFW cannot be initialized!")

#create the window
window = glfw.create_window(width, height, "Test: Shape", None, None)


if not window:
    glfw.terminate()
    raise Exception("Window cannot be created!")

#position the window on the screen
glfw.set_window_pos(window, 400, 200)


#set the callback function to window_resize
glfw.set_window_size_callback(window, window_resize)

#make the context current so OpenGL commands affect this window
glfw.make_context_current(window)


#each frame the background is cleared with this color.  Try changing it!
#values are rgba, 0.0 to 1.0
glClearColor(0.2, 0.2, 0.3, 1.0)


jewel_tones = {
    "emerald": [0.31, 0.78, 0.47],
    "amethyst": [0.6, 0.4, 0.8],
    "sapphire": [0.06, 0.32, 0.73],
    "ruby": [0.88, 0.07, 0.37],
    "topaz": [0.96, 0.67, 0.21],
    "turquoise": [0.25, 0.88, 0.82],
    "diamond": [0.85, 0.85, 0.95]
}


triangle = Shape(position=[0.0, 0.0, 0.0], color=jewel_tones["ruby"],  scale=0.2, rotation=0.33, sides=3)
square = Shape(position=[-0.25, 0.25, 0.0], color=jewel_tones["emerald"], scale=0.4, rotation=0.0, sides=4, static=False)
square.set_position(position=[-0.5, 0.5, 0.0])
pentagon = Shape(position=[0.25, 0.25, 0.0], color=jewel_tones["sapphire"], scale=0.2, sides=5, static=False)
pentagon.set_position(position=[0.5, 0.5, 0.0])
hexagon = Shape(position=[-0.5, -0.5, 0.0], color=jewel_tones["amethyst"], scale=0.2, sides=6, static=False)
hexagon.set_position(position=[-0.75, -0.5, 0.0])
circle = Shape(position=[0.5, -0.5, 0.0], color=jewel_tones["topaz"], scale=0.2, sides=30)
shapes = [triangle, square, pentagon, hexagon, circle]


while not glfw.window_should_close(window):
    #check for events (keyboard, mouse, etc)
    glfw.poll_events()
    #clear the screen to the background color
    glClear(GL_COLOR_BUFFER_BIT)

    pentagon.update_position(velocity=[0.0001 * (np.cos(glfw.get_time())*2.0), 0.0001 * (np.cos(glfw.get_time())*2.0), 0.0])
    square.update_rotation(delta_rotation=[0.0, 0.0, 0.0001])

    for shape in shapes:
        shape.draw()

    #swap the front and back buffers
    glfw.swap_buffers(window)


#terminate glfw, free up allocated resources
glfw.terminate()
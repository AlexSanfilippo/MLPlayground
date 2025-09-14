"""
WIP - Test the combination of our shape-drawing class (Shape) with Box2D physics.
"""
from src.graphics.physics_shape import PhysicsShape

"""
Visual tests for the class PhysicsShape
"""
from src.graphics.shape import Shape
import glfw
from OpenGL.GL import *
import numpy as np

from Box2D.b2 import world, polygonShape, staticBody, dynamicBody

#GLOBALS
#window width and height in pixels
width, height = 800, 800

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0.0, 0.0), doSleep=True)
PPM = 20.0  # pixels per meter
TARGET_FPS = 200
TIME_STEP = 1.0 / TARGET_FPS


def window_resize(window, width, height):
    """
    Automatically adjust image to acount for window resizing by user.
    """
    glViewport(0,0,width, height)


if not glfw.init():
    raise Exception("GLFW cannot be initialized!")

#create the window
window = glfw.create_window(width, height, "Test: PhysicsShape", None, None)


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

#creation of PhysicsShape objects
wall = PhysicsShape(color=jewel_tones["diamond"], position=[0.25, 0.23, 0.0], rotation=[0.0, 0.0,np.pi/4], scale=0.25, sides=4, static=False)
wall.make_physics_shape(world=world)
agent = PhysicsShape(position=[-0.5, 0.0, 0.0], color=jewel_tones["emerald"], rotation=np.pi/4 * 0.1, scale=0.1, sides=3, static=False)
agent.make_physics_shape(world=world)
agents = [wall, agent]
shapes = [wall, agent]

#Apply the force just ONCE to the agent
agent.physics_body.ApplyForce(force=(0.4, .05), point=agent.physics_body.worldCenter, wake=True)


while not glfw.window_should_close(window):
    #check for events (keyboard, mouse, etc)
    glfw.poll_events()
    #clear the screen to the background color
    glClear(GL_COLOR_BUFFER_BIT)

    #update physics world
    world.Step(TIME_STEP, 10, 10)

    #draw world
    for shape in shapes:
        shape.update_to_physics()
        shape.draw()

    #swap the front and back buffers
    glfw.swap_buffers(window)


#terminate glfw, free up allocated resources
glfw.terminate()
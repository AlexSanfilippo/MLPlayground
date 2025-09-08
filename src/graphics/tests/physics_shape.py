"""
WIP - Test the combination of our shape-drawing class (Shape) with Box2D physics.
"""

#Imagined interface
    #create a PhysicsShape of N sides
    #in main loop, update the physics world
    #in main loop, call update on all physics shapes to sync graphics to physics
    #draw all shapes

#TODO:
    #[]Physics shape should pass it's veritices to BOX2D to create a polygon shape
    #[]Physics shape should update it's position and rotation from the BOX2D body each frame
        #update() method
    #[]Add ability to apply forces to the physics shape
from graphics.physics_shape import PhysicsShape

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

from Box2D.b2 import world, polygonShape

#GLOBALS
#window width and height in pixels
width, height = 800, 800

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0.02, 0.0), doSleep=True)
PPM = width/10  # pixels per meter
TARGET_FPS = 200
TIME_STEP = 1.0 / TARGET_FPS


# Create a dynamic body
agent_position = [-0.8, 0]
dynamic_body = world.CreateDynamicBody(position=agent_position, angle=0)
# And add a box fixture onto it (with a nonzero density, so it will move)
box = dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)

# And a static body to hold the ground shape
ground_position = [2.2, 0]
ground_body = world.CreateStaticBody(
    position=ground_position,
    shapes=polygonShape(box=(.005, .005)),
)





def window_resize(window, width, height):
    """
    Automatically adjust image to acount for window resizing by user.
    """
    glViewport(0,0,width, height)


if not glfw.init():
    raise Exception("GLFW cannot be initialized!")

#create the window
window = glfw.create_window(width, height, "My First PyOpenGL Window", None, None)


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


wall = Shape(color=jewel_tones["diamond"], position=[*ground_position, 0.0], rotation=np.pi/4, scale=.8, sides=4, static=True)
agent = PhysicsShape(color=jewel_tones["emerald"], rotation=0, scale=0.1, sides=4, static=False)
agent.set_position([-0.8, 0.0, 0.0])
agent.set_rotation(np.pi/4)

shapes = [wall, agent]

while not glfw.window_should_close(window):
    #check for events (keyboard, mouse, etc)
    glfw.poll_events()
    #clear the screen to the background color
    glClear(GL_COLOR_BUFFER_BIT)

    #update physics world
    world.Step(TIME_STEP, 10, 10)

    #update agent_position
    agent.set_position(position=list(dynamic_body.position))

    #draw world
    for shape in shapes:
        shape.draw()

    #swap the front and back buffers
    glfw.swap_buffers(window)


#terminate glfw, free up allocated resources
glfw.terminate()
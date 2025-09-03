"""
A simple script to check that OpenGL is working.
"""
import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader


#Establish shaders
vertex_src = """
# version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;
out vec3 vColor;
void main(){
    gl_Position= vec4(aPos, 1.0);
    vColor = aColor;
}
"""

fragment_src = """
# version 330 core

in vec3 vColor;
out vec4 outColor;

void main(){
    outColor = vec4(vColor,1.0);
}
"""

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


#position (x,y,z) and color (r,g,b) for each vertex
vertices = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            -0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
            0.5, 0.5, 0.0, 1.0, 1.0, 1.0,]


#convert vertices to numpy array.  OpenGL needs a C-style array
vertices = np.array(vertices, dtype=np.float32)


#compile shaders
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src,GL_FRAGMENT_SHADER))


#Define the Vertex Buffer Object (VBO), which holds the vertices in GPU memory
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)


#Define the layout of the vertex data: position and color
position = glGetAttribLocation(shader, "aPos")
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
color = glGetAttribLocation(shader, "aColor")
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))


#tell OpenGL to use the shader program
glUseProgram(shader)


#each frame the background is cleared with this color.  Try changing it!
#values are rgba, 0.0 to 1.0
glClearColor(0.2, 0.2, 0.3, 1.0)


while not glfw.window_should_close(window):
    #check for events (keyboard, mouse, etc)
    glfw.poll_events()
    #clear the screen to the background color
    glClear(GL_COLOR_BUFFER_BIT)
    #tell OpenGL to draw the vertices as a triangle strip,
    #the 4 is the number of vertices to draw
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    #swap the front and back buffers
    glfw.swap_buffers(window)


#terminate glfw, free up allocated resources
glfw.terminate()
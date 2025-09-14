from pyglm import glm
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Shape:
    """
    Define a regular polygon to draw.
    """

    def __init__(self, position=[0.0, 0.0, 0.0], color=[1.0, 0.0, 1.0], scale=1.0, rotation=[0.0]*3, sides=3, shader=None, static=True):
        if static:
            self.position = position
        else:
            self.position = [0.0, 0.0, 0.0]
        self.color = color
        self.scale = scale
        if type(rotation) == list:
            self.rotation = glm.vec3(rotation)
        else:
            self.rotation = glm.vec3([0.0, 0.0, rotation])
        self.sides = sides
        self.static = static
        self.vertices = self.generate_vertices()
        self.indices = self.generate_indices()
        if shader:
            self.shader = shader
        else:
            if self.static:
                self.shader = self.get_static_shader()
            else:
                self.shader = self.get_moving_shader()
        self.setup()

    def get_static_shader(self):

        vertex_src = """// Vertex Shader
            #version 330 core

            layout(location = 0) in vec3 aPos;  // Vertex position
            layout(location = 1) in vec3 aColor; // Vertex color

            out vec3 vColor;  // Pass color to fragment shader

            void main() {
                gl_Position = vec4(aPos, 1.0);
                vColor = aColor;  // Pass color to fragment shader
        }"""

        fragment_src = """
            // Fragment Shader
            #version 330 core

            in vec3 vColor;  // Interpolated color from vertex shader
            out vec4 outColor;  // Final output color

            void main() {
                outColor = vec4(vColor, 1.0);  // Set output color with alpha = 1.0
            }
        """

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        return shader

    def get_moving_shader(self):

        vertex_src = """// Vertex Shader
            #version 330 core

            layout(location = 0) in vec3 aPos;  // Vertex position
            layout(location = 1) in vec3 aColor; // Vertex color

            uniform vec3 uPosition;  // Translation vector
            uniform vec3 uRotation;  // Rotation angles (in radians)

            out vec3 vColor;  // Pass color to fragment shader

            void main() {
                // Rotation matrices
                mat3 rotX = mat3(
                    1.0, 0.0, 0.0,
                    0.0, cos(uRotation.x), -sin(uRotation.x),
                    0.0, sin(uRotation.x), cos(uRotation.x)
                );

                mat3 rotY = mat3(
                    cos(uRotation.y), 0.0, sin(uRotation.y),
                    0.0, 1.0, 0.0,
                    -sin(uRotation.y), 0.0, cos(uRotation.y)
                );

                mat3 rotZ = mat3(
                    cos(uRotation.z), -sin(uRotation.z), 0.0,
                    sin(uRotation.z), cos(uRotation.z), 0.0,
                    0.0, 0.0, 1.0
                );

                // Apply rotation and translation
                vec3 transformedPos = rotZ * rotY * rotX * aPos + uPosition;

                gl_Position = vec4(transformedPos, 1.0);
                vColor = aColor;  // Pass color to fragment shader
        }"""

        fragment_src = """
            // Fragment Shader
            #version 330 core

            in vec3 vColor;  // Interpolated color from vertex shader
            out vec4 outColor;  // Final output color

            void main() {
                outColor = vec4(vColor, 1.0);  // Set output color with alpha = 1.0
            }
        """

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        return shader

    def setup(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * self.vertices.itemsize, ctypes.c_void_p(0))
        # color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * self.vertices.itemsize,
                              ctypes.c_void_p(3 * self.vertices.itemsize))

    def generate_vertices(self):
        vertices = []
        angle_step = 2 * np.pi / self.sides
        for i in range(self.sides):
            angle = i * angle_step + self.rotation.z
            x = self.position[0] + self.scale * np.cos(angle)
            y = self.position[1] + self.scale * np.sin(angle)
            z = self.position[2]
            vertices.extend([x, y, z, self.color[0], self.color[1], self.color[2]])
        self.rotation=[0.0, 0.0, 0.0]  # Reset rotation after generating vertices
        return np.array(vertices, dtype=np.float32)

    def generate_indices(self):
        indices = []
        for i in range(1, self.sides - 1):
            indices.extend([0, i, i + 1])
        return np.array(indices, dtype=np.uint32)

    def draw(self):
        glUseProgram(self.shader)
        glBindVertexArray(self.VAO)

        # Set transformation uniforms
        position_loc = glGetUniformLocation(self.shader, "uPosition")
        rotation_loc = glGetUniformLocation(self.shader, "uRotation")
        glUniform3fv(position_loc, 1, self.position)
        glUniform3fv(rotation_loc, 1, list(self.rotation))

        # Draw the shape
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

    def update_position(self, velocity):
        self.position = list(glm.vec3(self.position) + glm.vec3(velocity))

    def update_rotation(self, delta_rotation):
        self.rotation = list(glm.vec3(self.rotation) + glm.vec3(delta_rotation))

    def set_position(self, position):
        self.position = position

    def set_rotation(self, rotation):
        self.rotation = rotation




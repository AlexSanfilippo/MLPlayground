from src.graphics.shape import Shape
from Box2D.b2 import polygonShape
from Box2D.b2 import dynamicBody, staticBody
from OpenGL.GL import *

class PhysicsShape(Shape):
    """
    Define a regular polygon to draw with Box2D physics.
    """
    def __init__(self, position=[0.0, 0.0, 0.0], rotation=0.0, color=[1.0, 0.0, 1.0], scale=1.0, sides=3, static=False):
        super().__init__(position=position, rotation=rotation, color=color, scale=scale, sides=sides, static=static)
        self.physics_body = None
        self.position = position

    def create_box2d_polygon(vertices):
        """
        Takes a list of (x, y) tuples and returns a Box2D polygonShape.
        Only works for convex polygons.
        """
        return polygonShape(vertices=vertices)

    def make_physics_shape(self, world):
        """
        Create a Box2D physics body for the shape.
        """
        if self.static:
            body_type = staticBody
        else:
            body_type = dynamicBody
        # Convert vertices to (x, y) tuples for Box2D
        vertices_position_xy = [(float(self.vertices[i]), float(self.vertices[i + 1])) for i in range(len(self.vertices)) if i % 6 == 0]
        # Create the Box2D body
        if self.static:
            self.physics_body = world.CreateBody(type=body_type, position=(0, 0))
        else:
            self.physics_body = world.CreateBody(type=body_type, position=(self.position[0], self.position[1]))
        self.physics_body.CreatePolygonFixture(vertices=vertices_position_xy, density=1.0, friction=0.3)

    def get_physics_body(self):
        return self.physics_body

    def update_to_physics(self):
        if self.physics_body:
            self.position[0] = self.physics_body.position.x
            self.position[1] = self.physics_body.position.y
            self.rotation = [0.0, 0.0, -self.physics_body.angle]


    def draw(self):
        glUseProgram(self.shader)
        glBindVertexArray(self.VAO)

        # Set transformation uniforms
        position_loc = glGetUniformLocation(self.shader, "uPosition")
        rotation_loc = glGetUniformLocation(self.shader, "uRotation")
        glUniform3fv(position_loc, 1, [self.position[0], self.position[1], self.position[2]])
        glUniform3fv(rotation_loc, 1, list(self.rotation))

        # Draw the shape
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
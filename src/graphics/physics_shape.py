from graphics.shape import Shape


class PhysicsShape(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], rotation=0.0, color=[1.0, 0.0, 1.0], scale=1.0, sides=3, static=False):
        super().__init__(position=position, rotation=rotation, color=color, scale=scale, sides=sides, static=static)

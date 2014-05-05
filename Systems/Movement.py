import utils
import sdl2.ext


class Velocity(utils.Vector2D):

    def __init__(self, x=0, y=0):
        super(Velocity, self).__init__(x, y)


class MovementSystem(sdl2.ext.Applicator):

    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx, self.miny = minx, miny
        self.maxx, self.maxy = maxx, maxy

    def process(self, world, components):
        for v, s in components:
            s.x += v.x
            s.y += v.y

            s.x = max(s.x, self.minx)
            s.y = max(s.y, self.miny)

            width, height = s.size
            if s.x + width > self.maxx:
                s.x = self.maxx - width
            if s.y + height > self.maxy:
                s.y = self.maxy - height

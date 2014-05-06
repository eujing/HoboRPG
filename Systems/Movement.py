import utils
import sdl2.ext
import logging

logger = logging.getLogger(__name__)


class Velocity(utils.Vector2D):

    def __init__(self, x=0, y=0):
        utils.Vector2D.__init__(self, x, y)


class Position(utils.Vector2D):

    def __init__(self, x=0, y=0):
        utils.Vector2D.__init__(self, x, y)


class MovementSystem(sdl2.ext.Applicator):

    def __init__(self, minx, miny, maxx, maxy):
        sdl2.ext.Applicator.__init__(self)
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


class CollisionSystem(sdl2.ext.Applicator):

    def __init__(self):
        sdl2.ext.Applicator.__init__(self)
        self.is_applicator = True
        self.componenttypes = Velocity, sdl2.ext.Sprite

    def process(self, world, components):
        # Naive collision checking
        # Force components into a list as it is a generator
        # looping through a generator while looping through it
        # fucks shit up
        comps = list(components)
        for v, s in comps:
            if v.x != 0 or v.y != 0:
                for ov, os in comps:
                    if world.get_entities(v)[0] != world.get_entities(ov)[0]:
                        if int(s.x) == int(os.x) and int(s.y) == int(os.y):
                            s.x -= v.x
                            s.y -= v.y
                            v.x = 0
                            v.y = 0

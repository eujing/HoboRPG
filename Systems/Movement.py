from utils import Vector2D
from sdl2.ext import Applicator, Sprite
import logging

logger = logging.getLogger(__name__)


class Velocity(Vector2D):

    def __init__(self, x=0, y=0):
        Vector2D.__init__(self, x, y)


class Position(Vector2D):

    def __init__(self, x=0, y=0):
        Vector2D.__init__(self, x, y)


class Destination(Vector2D):

    def __init__(self, x=0, y=0):
        Vector2D.__init__(self, x, y)


class MovementSystem(Applicator):

    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, Sprite
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


class CollisionSystem(Applicator):

    def __init__(self):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, Sprite

    def process(self, world, components):
        # Naive collision checking
        # Force components into a list as it is a generator
        # looping through a generator while looping through it
        # fucks shit up
        comps = list(components)
        for v, s in comps:
            # Only check moving objects
            if v.x == 0 and v.y == 0:
                # continue
                pass
            for ov, os in comps:
                # Not the same object
                currEntity = world.get_entities(v)[0]
                otherEntity = world.get_entities(ov)[0]
                if currEntity != otherEntity:
                    # Collided
                    if int(s.x) == int(os.x) and int(s.y) == int(os.y):
                        s.x -= v.x
                        s.y -= v.y
                        v.x = 0
                        v.y = 0

                        logger.debug(
                            "{0} collided with {1}".format(
                                currEntity.__class__.__name__,
                                otherEntity.__class__.__name__))

                        if hasattr(otherEntity, "onCollide"):
                            getattr(otherEntity, "onCollide")(currEntity)

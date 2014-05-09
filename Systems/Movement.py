from utils import Vector2D, limit
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

class Collidable(object):

    def __init__(self, caller, effect=None):
        self.caller = caller
        self.effect = effect

    def doEffect(self, *arg):
        return self.effect(*arg)


class MovementSystem(Applicator):

    def __init__(self, gridWidth, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, Sprite
        self.minx, self.miny = minx, miny
        self.maxx, self.maxy = maxx, maxy
        self.gridWidth = gridWidth

    def process(self, world, components):
        for v, s in components:
            s.x = limit(s.x + v.x, self.minx, int(self.maxx - s.size[0]/self.gridWidth))
            s.y = limit(s.y + v.y, self.miny, int(self.maxy - s.size[1]/self.gridWidth))


class CollisionSystem(Applicator):

    def __init__(self):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, Sprite, Collidable

    def process(self, world, components):
        # Naive collision checking
        # Force components into a list as it is a generator
        # looping through a generator while looping through it
        # fucks shit up
        comps = list(components)
        n = 0
        for v, s, collidable in comps:
            # Only check moving objects
            # Results in some
            if v.x == 0 and v.y == 0 and collidable.effect is None:
                continue
            # for os in world.get_components((Sprite)):
            for ov, os, oCollidable in comps:
                # Not the same object
                currEntity = world.get_entities(s)[0]
                otherEntity = world.get_entities(os)[0]
                if currEntity != otherEntity:
                    n += 1
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

                        if collidable.effect is not None:
                            collidable.doEffect(otherEntity)
                        if oCollidable.effect is not None:
                            oCollidable.doEffect(currEntity)
            #logger.debug("Checked for {0} collisions in 1 pass".format(n))

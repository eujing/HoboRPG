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

    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, Position
        self.minx, self.miny = minx, miny
        self.maxx, self.maxy = maxx, maxy

    def process(self, world, components):
        for v, p in components:
            p.x = limit(p.x + v.x, self.minx, int(
                self.maxx - 1))
            p.y = limit(p.y + v.y, self.miny, int(
                self.maxy - 1))


class CollisionSystem(Applicator):

    def __init__(self):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, Sprite, Position, Collidable

    def process(self, world, components):
        # Naive collision checking
        # Force components into a list as it is a generator
        # looping through a generator while looping through it
        # fucks shit up
        comps = list(components)
        n = 0
        for v, s, p, collidable in comps:
            # Only check moving objects
            # Results in some
            if v.x == 0 and v.y == 0 and collidable.effect is None:
                continue
            # for os in world.get_components((Sprite)):
            for ov, os, op, oCollidable in comps:
                # Not the same object
                currEntity = world.get_entities(s)[0]
                otherEntity = world.get_entities(os)[0]
                if currEntity != otherEntity:
                    n += 1
                    # Collided
                    if int(p.x) == int(op.x) and int(p.y) == int(op.y):
                        p.x -= v.x
                        p.y -= v.y
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

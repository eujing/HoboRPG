import logging
import Systems.Mapping

from Utils import Vector2D, autoslot
from Ecs import HSystem
from sdl2.ext import Sprite

logger = logging.getLogger(__name__)


@autoslot
class Velocity(Vector2D):

    def __init__(self, x=0, y=0):
        Vector2D.__init__(self, x, y)


@autoslot
class Position(Vector2D):

    def __init__(self, mapName, x=0, y=0):
        super(Position, self).__init__(x, y)
        self.mapName = mapName


@autoslot
class Destination(Vector2D):

    def __init__(self, mapName, x=0, y=0):
        super(Destination, self).__init__(x, y)
        self.mapName = mapName


@autoslot
class Collidable(object):

    def __init__(self, caller, effect=None):
        self.caller = caller
        self.effect = effect

    def doEffect(self, *arg):
        return self.effect(*arg)


class MovementSystem(HSystem):

    def __init__(self):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, Position
        self.topLeft = None
        self.bottomRight = None
        self.eventListeners[Systems.Mapping.MapChangeEvent] = self.mapChangeHandler

    def mapChangeHandler(self, mapChangeEvent):
        self.topLeft = Position(0, 0)
        self.bottomRight = Position(mapChangeEvent.map.name, mapChangeEvent.map.size[0] - 1, mapChangeEvent.map.size[1] - 1)

    def process(self, world, components):
        for v, p in components:
            p += v
            p.limit(self.topLeft, self.bottomRight)


class CollisionSystem(HSystem):

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
                        p -= v
                        v.x = 0
                        v.y = 0

                        # logger.debug(
                        #     "{0} collided with {1}".format(
                        #         currEntity.__class__.__name__,
                        #         otherEntity.__class__.__name__))

                        if collidable.effect is not None:
                            collidable.doEffect(world, otherEntity)
                        if oCollidable.effect is not None:
                            oCollidable.doEffect(world, currEntity)
            #logger.debug("Checked for {0} collisions in 1 pass".format(n))

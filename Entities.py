from Systems.Movement import Collidable, Velocity
from sdl2.ext import Entity
from Utils import autoslot


@autoslot
class Player(Entity):

    def __init__(self, world, sprite, pos):
        self.sprite = sprite
        self.position = pos
        self.velocity = Velocity()
        self.collidable = Collidable(self)


@autoslot
class Wall(Entity):

    def __init__(self, world, sprite, pos):
        self.sprite = sprite
        self.position = pos
        self.velocity = Velocity()
        self.collidable = Collidable(self)


@autoslot
class Teleporter(Entity):

    def __init__(self, world, sprite, pos=(0, 0), dest=(0, 0)):
        self.sprite = sprite
        self.position = pos
        self.velocity = Velocity()
        self.destination = dest
        self.collidable = Collidable(self, effect=self.onCollide)

    def onCollide(self, world, other):
        p = other.position
        p.mapName = self.destination.mapName
        p.x = self.destination.x
        p.y = self.destination.y

import sdl2
import sdl2.ext
from sdl2.ext import Entity, Color
import logging
import random

from Systems.Renderer import ConsoleRenderer
from Systems.Movement import Collidable, Destination, Position, Velocity, MovementSystem, CollisionSystem
from utils import autoslot
from ecs import World

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Player(Entity):

    def __init__(self, world, sprite, x=0, y=0):
        self.sprite = sprite
        self.position = Position(x, y)
        self.velocity = Velocity()
        self.collidable = Collidable(self)


@autoslot
class Wall(Entity):

    def __init__(self, world, sprite, x=0, y=0):
        self.sprite = sprite
        self.position = Position(x, y)
        self.velocity = Velocity()
        self.collidable = Collidable(self)


class Teleporter(Entity):

    def __init__(self, world, sprite, pos=(0, 0), dest=(0, 0)):
        self.sprite = sprite
        self.position = Position(*pos)
        self.velocity = Velocity()
        self.destination = Destination(*dest)
        self.collidable = Collidable(self, effect=self.onCollide)

    def onCollide(self, other):
        p = other.position
        p.x = self.destination.x
        p.y = self.destination.y


def main():
    UNIT_LENGTH = 10
    sdl2.ext.init()
    window = sdl2.ext.Window("HoboRPG", size=(800, 400))
    window.show()

    world = World()
    consoleRenderer = ConsoleRenderer(
        window, UNIT_LENGTH, [0, 0, 80, 40], (160, 80))
    collisionSystem = CollisionSystem()
    movementSystem = MovementSystem(0, 0, 160, 80)

    world.add_system(movementSystem)
    world.add_system(collisionSystem)
    world.add_system(consoleRenderer)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    whiteSprite = factory.from_color(
        Color(255, 255, 255), size=(UNIT_LENGTH, UNIT_LENGTH))
    player = Player(world, whiteSprite, x=0, y=0)
    consoleRenderer.setPlayer(player)

    greenSprite = factory.from_color(
        Color(0, 255, 0), size=(UNIT_LENGTH, UNIT_LENGTH))
    Teleporter(world, greenSprite, pos=(0, 4), dest=(1, 5))
    greenSprite2 = factory.from_color(
        Color(0, 255, 0), size=(UNIT_LENGTH, UNIT_LENGTH))
    Teleporter(world, greenSprite2, pos=(1, 5), dest=(2, 6))

    xCoords = [random.randint(0, 160) for i in range(50)]
    yCoords = [random.randint(0, 80) for i in range(50)]
    for x, y in set(zip(xCoords, yCoords)):
        if (x, y) in ((0, 0), (0, 4), (1, 5)):
            continue
        redSprite = factory.from_color(
            Color(255, 0, 0), size=(UNIT_LENGTH, UNIT_LENGTH))
        Wall(world, redSprite, x, y)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

            if event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                if key == sdl2.SDLK_w:
                    player.velocity.y = -1
                elif key == sdl2.SDLK_s:
                    player.velocity.y = 1
                elif key == sdl2.SDLK_a:
                    player.velocity.x = -1
                elif key == sdl2.SDLK_d:
                    player.velocity.x = 1

            if event.type == sdl2.SDL_KEYUP:
                key = event.key.keysym.sym
                if key in (sdl2.SDLK_w, sdl2.SDLK_s):
                    player.velocity.y = 0
                if key in (sdl2.SDLK_a, sdl2.SDLK_d):
                    player.velocity.x = 0

        sdl2.SDL_Delay(10)
        world.process()
    return 0

if __name__ == "__main__":
    main()

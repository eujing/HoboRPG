import sdl2
import sdl2.ext
import logging

from sdl2.ext import SpriteFactory, Color
from Entities import Player
from Systems.Renderer import ConsoleRenderer
from Systems.Movement import Position, MovementSystem, CollisionSystem
from Systems.Mapping import MapSystem, MapRequestEvent
from Ecs import HWorld

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    # Sets the number of pixels the width of a grid cell should be
    UNIT_LENGTH = 10
    sdl2.ext.init()
    window = sdl2.ext.Window("HoboRPG", size=(800, 400))
    window.show()

    world = HWorld()
    consoleRenderer = ConsoleRenderer(window, UNIT_LENGTH, [0, 0, 80, 40])
    collisionSystem = CollisionSystem()
    movementSystem = MovementSystem()
    mapSystem = MapSystem(world, UNIT_LENGTH)

    # Create a player
    factory = SpriteFactory(sdl2.ext.SOFTWARE)
    whiteSprite = factory.from_color(Color(255, 255, 255), size=(UNIT_LENGTH, UNIT_LENGTH))
    player = Player(world, whiteSprite, Position("world", 0, 0))
    consoleRenderer.setPlayer(player)

    world.add_system(mapSystem)
    world.add_system(movementSystem)
    world.add_system(collisionSystem)
    world.add_system(consoleRenderer)

    world.postEvent(MapRequestEvent("world"))

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

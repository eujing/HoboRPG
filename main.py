import sdl2
import sdl2.ext

from Systems.Renderer import SoftwareRenderer
from Systems.Movement import Velocity, MovementSystem, CollisionSystem


class Player(sdl2.ext.Entity):

    def __init__(self, world, sprite, x=0, y=0):
        self.sprite = sprite
        self.sprite.position = x, y
        self.velocity = Velocity()


class Wall(sdl2.ext.Entity):

    def __init__(self, world, sprite, x=0, y=0):
        self.sprite = sprite
        self.sprite.position = x, y
        self.velocity = Velocity()


def main():
    UNIT_LENGTH = 20
    sdl2.ext.init()
    window = sdl2.ext.Window("HoboRPG", size=(800, 400))
    window.show()

    world = sdl2.ext.World()
    spriteRenderer = SoftwareRenderer(window)
    collisionSystem = CollisionSystem()
    movementSystem = MovementSystem(0, 0, 800, 400)

    world.add_system(movementSystem)
    world.add_system(collisionSystem)
    world.add_system(spriteRenderer)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    whiteSprite = factory.from_color(
        sdl2.ext.Color(255, 255, 255), size=(UNIT_LENGTH, UNIT_LENGTH))
    player = Player(world, whiteSprite, x=0, y=0)

    for i in range(10):
        redSprite = factory.from_color(sdl2.ext.Color(255, 0, 0), size=(UNIT_LENGTH, UNIT_LENGTH))
        Wall(world, redSprite, i*UNIT_LENGTH, 3*UNIT_LENGTH)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_w:
                    player.velocity.y = -UNIT_LENGTH
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    player.velocity.y = UNIT_LENGTH
                elif event.key.keysym.sym == sdl2.SDLK_a:
                    player.velocity.x = -UNIT_LENGTH
                elif event.key.keysym.sym == sdl2.SDLK_d:
                    player.velocity.x = UNIT_LENGTH
            if event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_w, sdl2.SDLK_s):
                    player.velocity.y = 0
                if event.key.keysym.sym in (sdl2.SDLK_a, sdl2.SDLK_d):
                    player.velocity.x = 0

        sdl2.SDL_Delay(30)
        world.process()
    return 0

if __name__ == "__main__":
    main()

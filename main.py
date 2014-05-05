import sdl2
import sdl2.ext

from Systems.Renderer import SoftwareRenderer
from Systems.Movement import Velocity, MovementSystem


class Player(sdl2.ext.Entity):

    def __init__(self, world, sprite, x=0, y=0):
        self.sprint = sprite
        self.sprite.pos = x, y
        self.velocity = Velocity()


def main():
    sdl2.ext.init()
    window = sdl2.ext.Window("HoboRPG", size=(800, 400))
    window.show()

    world = sdl2.ext.World()
    spriteRenderer = SoftwareRenderer(window)
    movementSystem = MovementSystem(0, 0, 800, 400)

    world.add_system(movementSystem)
    world.add_system(spriteRenderer)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    character = factory.from_color(
        sdl2.ext.Color(255, 255, 255), size=(12, 12))
    player = Player(world, character, x=0, y=0)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_w:
                    player.velocity.y = -5
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    player.velocity.y = 5
                elif event.key.keysym.sym == sdl2.SDLK_a:
                    player.velocity.x = -5
                elif event.key.keysym.sym == sdl2.SDLK_d:
                    player.velocity.x = 5
            if event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_w, sdl2.SDLK_s):
                    player.velocity.y = 0
                elif event.key.keysym.sym in (sdl2.SDLK_a, sdl2.SDLK_d):
                    player.velocity.x = 0

        sdl2.SDL_Delay(10)
        world.process()
    return 0

if __name__ == "__main__":
    main()

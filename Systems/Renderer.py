import sdl2.ext
import sdl2.rect
import sdl2.video
from sdl2.surface import SDL_BlitSurface
from utils import limit
import collections


class ConsoleRenderer(sdl2.ext.SoftwareSpriteRenderSystem):

    def __init__(self, window, gridWidth, viewport, mapSize):
        super(ConsoleRenderer, self).__init__(window)
        self.gridWidth = gridWidth
        self.viewport = viewport
        self.mapSize = mapSize
        self.player = None

    def setPlayer(self, player):
        self.player = player

    def updateViewport(self):
        if self.player is None:
            return

        s = self.player.sprite
        v = self.player.velocity

        horizontalHalf = self.viewport[0] + self.viewport[2] / 2
        if s.x < horizontalHalf and v.x < 0 or s.x >= horizontalHalf and v.x > 0:
            self.viewport[0] += v.x

        verticalHalf = self.viewport[1] + self.viewport[3] / 2
        if s.y < verticalHalf and v.y < 0 or s.y >= verticalHalf and v.y > 0:
            self.viewport[1] += v.y

        self.viewport[0] = limit(self.viewport[0], 0, self.mapSize[0] - self.viewport[2])
        self.viewport[1] = limit(self.viewport[1], 0, self.mapSize[1] - self.viewport[3])

    def inViewport(self, sprite):
        return self.viewport[0] <= sprite.x < self.viewport[0] + self.viewport[2] and \
            self.viewport[1] <= sprite.y < self.viewport[1] + self.viewport[3]

    def drawSprite(self, sprite, r):
        r.x = (sprite.x - self.viewport[0]) * self.gridWidth
        r.y = (sprite.y - self.viewport[1]) * self.gridWidth
        SDL_BlitSurface(sprite.surface, None, self.surface, r)

    def render(self, sprites):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))

        self.updateViewport()
        r = sdl2.rect.SDL_Rect(0, 0, 0, 0)
        if isinstance(sprites, collections.Iterable):
            for s in sprites:
                if self.inViewport(s):
                    self.drawSprite(s, r)
        else:
            if self.inViewport(s):
                self.drawSprite(sprites, r)
        sdl2.video.SDL_UpdateWindowSurface(self.window)

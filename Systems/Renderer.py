import sdl2.ext
import sdl2.rect
import sdl2.video
from sdl2.surface import SDL_BlitSurface
from utils import limit
from Systems.Movement import Position
import collections


class ConsoleRenderer(sdl2.ext.SoftwareSpriteRenderSystem, sdl2.ext.Applicator):

    def __init__(self, window, gridWidth, viewport, mapSize):
        super(ConsoleRenderer, self).__init__(window)
        self.componenttypes = (sdl2.ext.Sprite, Position)
        self.gridWidth = gridWidth
        self.viewport = viewport
        self.mapSize = mapSize
        self.player = None

    def setPlayer(self, player):
        self.player = player

    def updateViewport(self):
        if self.player is None:
            return

        p = self.player.position
        v = self.player.velocity

        horizontalHalf = self.viewport[0] + self.viewport[2] / 2
        if p.x < horizontalHalf and v.x < 0 or p.x >= horizontalHalf and v.x > 0:
            self.viewport[0] += v.x

        verticalHalf = self.viewport[1] + self.viewport[3] / 2
        if p.y < verticalHalf and v.y < 0 or p.y >= verticalHalf and v.y > 0:
            self.viewport[1] += v.y

        self.viewport[0] = limit(self.viewport[0], 0, self.mapSize[0] - self.viewport[2])
        self.viewport[1] = limit(self.viewport[1], 0, self.mapSize[1] - self.viewport[3])

    def inViewport(self, position):
        return self.viewport[0] <= position.x < self.viewport[0] + self.viewport[2] and \
            self.viewport[1] <= position.y < self.viewport[1] + self.viewport[3]

    def drawSprite(self, sprite, position, r):
        r.x = (position.x - self.viewport[0]) * self.gridWidth
        r.y = (position.y - self.viewport[1]) * self.gridWidth
        SDL_BlitSurface(sprite.surface, None, self.surface, r)

    def process(self, world, components):
        self.render(sorted(components, key=lambda c: c[0].depth))

    def render(self, comps):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))

        self.updateViewport()
        r = sdl2.rect.SDL_Rect(0, 0, 0, 0)
        if isinstance(comps, collections.Iterable):
            for s, p in comps:
                if self.inViewport(p):
                    self.drawSprite(s, p, r)
        else:
            if self.inViewport(comps[1]):
                self.drawSprite(comps[0], r)
        sdl2.video.SDL_UpdateWindowSurface(self.window)

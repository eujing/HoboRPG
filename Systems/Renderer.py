import sdl2.ext
import sdl2.rect
import sdl2.video
import collections
import logging
import Systems.Mapping
import Systems.Movement

from sdl2.surface import SDL_BlitSurface
from Utils import limit
from Ecs import HSystem


logger = logging.getLogger()


class ConsoleRenderer(sdl2.ext.SoftwareSpriteRenderSystem, HSystem):
    """
    Handles the rendering of entities with Sprites and Positions
    Also allows for scrolling via a viewport
    """

    def __init__(self, window, gridWidth, viewport):
        """
        Initializes ConsoleRenderer object

        Args:
            window: window to be rendered to
            gridWidth: width of a unit length in pixels
            viewport: a list of 4 values (x, y, w, h) describing the viewport
        """
        super(ConsoleRenderer, self).__init__(window)
        self.componenttypes = (sdl2.ext.Sprite, Systems.Movement.Position)
        self.gridWidth = gridWidth
        self.viewport = viewport
        self.map = None
        self.player = None
        self.eventListeners[Systems.Mapping.MapChangeEvent] = self.mapChangeHandler

    def mapChangeHandler(self, mapChangeEvent):
        """
        Changes map being rendered to the new current map

        Args:
            mapChangeEvent: A MapChangeEvent object
        """
        self.map = mapChangeEvent.map
        self.viewport[0] = 0
        self.viewport[1] = 0

    def setPlayer(self, player):
        self.player = player

    def updateViewport(self):
        """
        Updates the coordinates of the viewport to track the player's position
        """
        if self.player is None:
            return

        if self.map is None:
            return

        p = self.player.position
        v = self.player.velocity

        # Check if Player has gone past half of the screen horizontally
        horizontalHalf = self.viewport[0] + self.viewport[2] / 2
        if p.x < horizontalHalf and v.x < 0 or p.x >= horizontalHalf and v.x > 0:
            self.viewport[0] += v.x

        # Check if Player has gone past half of the screen vertically
        verticalHalf = self.viewport[1] + self.viewport[3] / 2
        if p.y < verticalHalf and v.y < 0 or p.y >= verticalHalf and v.y > 0:
            self.viewport[1] += v.y

        self.viewport[0] = limit(self.viewport[0], 0, self.map.size[0] - self.viewport[2])
        self.viewport[1] = limit(self.viewport[1], 0, self.map.size[1] - self.viewport[3])

    def inViewport(self, position):
        return self.viewport[0] <= position.x < self.viewport[0] + self.viewport[2] and \
            self.viewport[1] <= position.y < self.viewport[1] + self.viewport[3]

    def drawSprite(self, sprite, position, r):
        r.x = (position.x - self.viewport[0]) * self.gridWidth
        r.y = (position.y - self.viewport[1]) * self.gridWidth
        SDL_BlitSurface(sprite.surface, None, self.surface, r)

    def process(self, world, components):
        """
        Tracks the map the player is in and requests for a map change accordingly.
        Also calls the rendering method

        Args:
            world: The current world
            components: Tuples of (Sprite, Position)
        """
        # Check if player has transitioned into another map
        if self.player.position.mapName != self.map.name:
            world.postEvent(Systems.Mapping.MapRequestEvent(self.player.position.mapName))
        self.render(sorted(components, key=lambda c: c[0].depth))

    def render(self, comps):
        """
        Renders all Entities with a Sprite and Position

        Args:
            comps: Sorted tuples of (Sprite, Position)
        """
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

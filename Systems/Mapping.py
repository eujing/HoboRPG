import logging
import random
import sdl2
import Entities
import Systems.Movement

from sdl2.ext import SpriteFactory, Color
from Ecs import HSystem


logger = logging.getLogger(__name__)


class Map(object):
    """
    Wraps the tracking of entities relevant to the current map
    and helper methods for creating a map
    """

    def __init__(self, name, size):
        self.name = name
        self.size = size

        # A store for repeating sprites
        self.spriteStore = []

        # Values are indexes that map Sprites in spriteStore
        self.grid = [[-1] * size[1] for _ in range(size[0])]

        # Keep track of created entities
        self.entities = []

    def setSprite(self, entity):
        """
        Helper method for creating a map with Entities
        Caches repeating sprites to save memory

        Args:
            entity: Entities that have a Sprite and Position
        """
        self.entities.append(entity)
        sprite = entity.sprite
        pos = entity.position

        if sprite in self.spriteStore:
            self.grid[pos.x][pos.y] = self.spriteStore.index(sprite)
        else:
            self.spriteStore.append(sprite)
            self.grid[pos.x][pos.y] = len(self.spriteStore) - 1

    def getSprite(self, pos):
        """
        Helper method for getting a sprite at a position

        Args:
            pos: A Position indicating the position of the sprite
        """
        index = self.grid[pos.x][pos.y]
        if index == -1:
            return None
        else:
            return self.spriteStore[index]


class MapRequestEvent(object):
    """
    For requesting a change in map
    """

    def __init__(self, mapName):
        self.mapName = mapName


class MapChangeEvent(object):
    """
    To notify that the map has been changed
    """

    def __init__(self, newMap):
        self.map = newMap


class MapSystem(HSystem):
    """
    Handles requests for maps and the loading/creation/changing of maps
    """

    def __init__(self, world, gridWidth):
        """
        Initializes a MapSystem

        Args:
            world: world where all entities are stored
            gridWidth: width of a unit length in pixels
        """
        super(MapSystem, self).__init__()
        self.gridWidth = gridWidth
        self.world = world
        self.eventListeners[MapRequestEvent] = self.mapRequestHandler
        self.componenttypes = tuple()
        self.currMap = None

    def mapRequestHandler(self, mapRequestEvent):
        """
        Handles a request for map change

        Args:
            mapRequestEvent: A MapRequestEvent object
        """
        logger.debug("Generating map: {0}".format(mapRequestEvent.mapName))
        m = None

        # Handle map changes
        if mapRequestEvent.mapName == "world":
            m = self.getWorldMap((160, 80))
            self.world.postEvent(MapChangeEvent(m))
        elif mapRequestEvent.mapName == "world2":
            m = self.getWorld2Map((160, 80))
            self.world.postEvent(MapChangeEvent(m))

        # Remove all relevant entities before adding more
        if self.currMap is not None:
            for e in self.currMap.entities:
                e.delete()

        self.currMap = m

    def getWorldMap(self, size):
        m = Map("world", size)

        factory = SpriteFactory(sdl2.ext.SOFTWARE)

        # Create teleporters
        greenSprite = factory.from_color(Color(0, 255, 0), size=(self.gridWidth, self.gridWidth))
        positions = ((0, 4), (1, 5))
        destinations = ((1, 5), (2, 6))
        for p, d in zip(positions, destinations):
            pos = Systems.Movement.Position("world", *p)
            dest = Systems.Movement.Destination("world", *d)
            m.setSprite(Entities.Teleporter(self.world, greenSprite, pos=pos, dest=dest))

        blueSprite = factory.from_color(Color(0, 0, 255), size=(self.gridWidth, self.gridWidth))
        pos = Systems.Movement.Position("world", 10, 10)
        dest = Systems.Movement.Destination("world2", 0, 0)
        m.setSprite(Entities.Teleporter(self.world, blueSprite, pos=pos, dest=dest))

        # Create walls
        xCoords = [random.randint(0, 159) for i in range(50)]
        yCoords = [random.randint(0, 79) for i in range(50)]
        wallSprite = factory.from_color(Color(255, 0, 0), size=(self.gridWidth, self.gridWidth))
        for x, y in set(zip(xCoords, yCoords)):
            if (x, y) in ((0, 0), (0, 4), (1, 5), (10, 10)):
                continue
            pos = Systems.Movement.Position("world", x, y)
            m.setSprite(Entities.Wall(self.world, wallSprite, pos))

        return m

    def getWorld2Map(self, size):
        m = Map("world2", size)

        factory = SpriteFactory(sdl2.ext.SOFTWARE)

        blueSprite = factory.from_color(Color(0, 0, 255), size=(self.gridWidth, self.gridWidth))
        pos = Systems.Movement.Position("world2", 5, 5)
        dest = Systems.Movement.Destination("world", 0, 0)
        m.setSprite(Entities.Teleporter(self.world, blueSprite, pos=pos, dest=dest))

        return m

    def process(self, world, components):
        pass

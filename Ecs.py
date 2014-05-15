import logging

from sdl2.ext import World, Applicator
from collections import defaultdict

logger = logging.getLogger(__name__)


class HSystem(Applicator):
    """
    Has event listening capabilities
    """

    def __init__(self):
        super(HSystem, self).__init__()
        self.eventListeners = {}


class HWorld(World):
    """
    Has event listening capabilities
    """

    def __init__(self):
        super(HWorld, self).__init__()
        self.eventListeners = defaultdict(list)

    def add_system(self, system):
        super(HWorld, self).add_system(system)
        for eventType, listener in system.eventListeners.items():
            self.eventListeners[eventType].append(listener)

    def postEvent(self, event):
        """
        Posts an event to all relevant listeners in the world

        Args:
            event: Any object representing an event
        """
        if event.__class__ in self.eventListeners:
            for listener in self.eventListeners[event.__class__]:
                listener(event)

import logging

from sdl2.ext import World, Applicator
from collections import defaultdict

logger = logging.getLogger(__name__)


class HSystem(Applicator):

    def __init__(self):
        super(HSystem, self).__init__()
        self.eventListeners = {}


class HWorld(World):

    def __init__(self):
        super(HWorld, self).__init__()
        self.eventListeners = defaultdict(list)

    def add_system(self, system):
        super(HWorld, self).add_system(system)
        for eventType, listener in system.eventListeners.items():
            self.eventListeners[eventType].append(listener)

    def postEvent(self, event):
        if event.__class__ in self.eventListeners:
            for listener in self.eventListeners[event.__class__]:
                listener(event)

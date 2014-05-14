from sdl2.ext import World, System
from collections import defaultdict


class HSystem(System):

    def __init__(self):
        super(HSystem, self).__init__()
        self.eventListeners = {}


class HWorld(World):

    def __init__(self):
        super(HWorld, self).__init__()
        self.eventListeners = defaultdict(list)

    def add_system(self, system):
        super(HWorld, self).add_system(system)
        for event, listener in system.eventListeners:
            self.eventListeners[event].append(listener)

    def postEvent(self, event):
        if event.__class__ in self.eventListeners:
            for listener in self.eventListeners:
                listener(event)

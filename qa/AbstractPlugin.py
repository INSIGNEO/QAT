import os

class AbstractPlugin:
    def __init__(self):
        self.Parameters = {}

    def setPluginParameters(self, **kargs):
        self.Parameters = kargs

    def execute(self):
        pass

from core.component import Component

class Source(Component):
    def __init__(self, posX, posY, voltage):
        super().__init__("assets/sprites/source.png", posX, posY)
        self.voltage = voltage
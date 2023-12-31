from core.component import Component

class Resistance(Component):
    def __init__(self, posX, posY, resistance):
        super().__init__("assets/sprites/resistance.png", posX, posY, True)
        self.resistance = resistance
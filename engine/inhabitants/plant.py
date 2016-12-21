from engine.inhabitants.inhabitant import Inhabitant

class WaterPlant(Inhabitant):
    """
    Water plant. Can be eaten by prey fishes and snails.
    """
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 3.0
    
    @Inhabitant.can_eat()
    def eat(self, inhabitant):
        return super(WaterPlant, self).eat(inhabitant)
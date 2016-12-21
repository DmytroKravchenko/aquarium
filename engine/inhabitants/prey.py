from engine.inhabitants.inhabitant import Inhabitant
from engine.inhabitants.predator import PredatorFish

class PreyFish(Inhabitant):
    """
    Prey fish eats water plants and may be eaten by predator fish
    """
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 9.0
    
    @Inhabitant.can_eat('WaterPlant', 'PredatorFish')
    def eat(self, inhabitant):
        if isinstance(inhabitant, PredatorFish):
            return inhabitant.eat(self)
        else:
            return super(PreyFish, self).eat(inhabitant)

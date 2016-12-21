from engine.inhabitants.inhabitant import Inhabitant

class PredatorFish(Inhabitant):
    """
    Predator fish eats prey fishes. 
    If prey fish try to eat predator, the predator eats prey fish.
    """
    MIN_WEIGHT = 10.0
    MAX_WEIGHT = 10.0
    
    @Inhabitant.can_eat('PreyFish')
    def eat(self, inhabitant):
        return super(PredatorFish, self).eat(inhabitant)

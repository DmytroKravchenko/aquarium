from engine.inhabitants.inhabitant import Inhabitant

   
class Snail(Inhabitant):
    """
    Snail can eat water plants
    """
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 5.0
    
    @Inhabitant.can_eat('WaterPlant')
    def eat(self, inhabitant):
        return super(Snail, self).eat(inhabitant)
        
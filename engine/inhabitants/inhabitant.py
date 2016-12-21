""" """

class Inhabitant(object):
    """
    Inhabitant of the aquarium.
    Used as blueprint.
    """
    MIN_WEIGHT = 0.0
    MAX_WEIGHT = 10.0
    
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.__initial_weight = weight
        self.eated = []
      
    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, weight):
        if weight < self.MIN_WEIGHT or weight > self.MAX_WEIGHT:
            raise Exception("Weight of {0} must be in range [{1}..{2}] kg".format(
                self.__class__.__name__, PreyFish.MIN_WEIGHT, PreyFish.MAX_WEIGHT))
            
        self.__weight = weight  

    @staticmethod
    def can_eat(*ration):
        def eats_decorator(func):
            def func_wrapper(self, prey):
                if prey.__class__.__name__ in ration:
                    return func(self, prey)
                else:
                    return None
            return func_wrapper
        return eats_decorator
        
    def eat(self, inhabitant):
        # can't eat oneself
        if self is inhabitant:
            return None
            
        self.eated.append(inhabitant)
        self.__weight += inhabitant.weight
        return inhabitant
    
    def __repr__(self):
        return '<{0} {1}: {2} kg>'.format(self.__class__.__name__, self.name, round(self.weight, 3) )
                

from random import choice, sample, randint, random

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
                
                
class WaterPlant(Inhabitant):
    """
    Water plant. Can be eaten by prey fishes and snails.
    """
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 3.0
    
    @Inhabitant.can_eat()
    def eat(self, inhabitant):
        return super(WaterPlant, self).eat(inhabitant)

    
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

   
class Snail(Inhabitant):
    """
    Snail can eat water plants
    """
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 5.0
    
    @Inhabitant.can_eat('WaterPlant')
    def eat(self, inhabitant):
        return super(Snail, self).eat(inhabitant)
        

POSSIBLE_INHABITANTS = (PreyFish, PredatorFish, WaterPlant, Snail)


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

        
class Aquarium(object):
    """
    Class represents the aquarium
    """
    __metaclass__ = Singleton 
    
    MIN_INHABITANTS = 20
    MAX_INHABITANTS = 100
    
    PAIRS_OF_EATING = [ (PreyFish, WaterPlant), 
                        (Snail, WaterPlant), 
                        (PredatorFish, PreyFish) ]
    
    def __init__(self, quantity):
        if quantity < Aquarium.MIN_INHABITANTS \
                or quantity > Aquarium.MAX_INHABITANTS:
            raise Exception("Quantity of inhabitants must be in [{0}..{1}]"\
                .format(Aquarium.MIN_INHABITANTS, Aquarium.MAX_INHABITANTS))
        self.inhabitants = []
        self.populate(quantity)
        
    def get_random_inhabitant(self, name):
        inhabitant_class = choice(POSSIBLE_INHABITANTS)
        
        weight_rand_difference = random() * (inhabitant_class.MAX_WEIGHT - inhabitant_class.MIN_WEIGHT)
        inhabitant_weight = inhabitant_class.MIN_WEIGHT + weight_rand_difference
        
        return inhabitant_class(name, inhabitant_weight)
    
    def populate(self, quantity): 
        self.inhabitants = [self.get_random_inhabitant(str(i + 1)) for i in range(quantity)]
    
    def evalute_inhabitants(self):
        while self.thing_to_eat():
            subject, food = sample(self.inhabitants, 2)
            remains = subject.eat(food)
            if remains in self.inhabitants:
                self.inhabitants.remove(remains)
            
    def thing_to_eat(self):
        inhabitants_classes = set(inhabitant.__class__ for inhabitant in self.inhabitants)
        return any(set(pair).issubset(inhabitants_classes) for pair in Aquarium.PAIRS_OF_EATING)
    
    def __repr__(self):
        result = 'Aquarium include {0} inhabitants: \n'.format(len(self.inhabitants))
        
        def weight_sorted_output(_class):
            inhabitants = [inhabitant for inhabitant in self.inhabitants if inhabitant.__class__ is _class]
            ranged_inhabitants = sorted(inhabitants, key=lambda x: -x.weight)
            return _class.__name__, ranged_inhabitants
        
        def out_inhabitant_list(inahabitant_list, level='\t', modifier='\t'):
            result = ''
            for inhabitant in inahabitant_list:
                result += level + repr(inhabitant) + '\n'
                if inhabitant.eated:
                    result += level + modifier \
                        + 'eated:\n' + out_inhabitant_list(inhabitant.eated, level + modifier)
            return result
        
        inhabitant_groups = [
            weight_sorted_output(PreyFish),
            weight_sorted_output(PredatorFish),
            weight_sorted_output(Snail),
            weight_sorted_output(WaterPlant) 
            ]
        
        for group in inhabitant_groups:
            inhabitant_type, inhabitants_list = group
            if inhabitants_list:
                result += '\n {0}: \n {1}'.format(inhabitant_type, out_inhabitant_list(inhabitants_list)) 
           
        return result
   
if __name__ == '__main__':
    inhabitants_quantity = 90
    aquarium = Aquarium(inhabitants_quantity)
    print(aquarium)
    aquarium.evalute_inhabitants()
    print(aquarium)

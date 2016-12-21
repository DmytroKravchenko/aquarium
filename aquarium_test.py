import unittest

from engine.aquarium import Aquarium
from engine.inhabitants.plant import WaterPlant
from engine.inhabitants.prey import PreyFish
from engine.inhabitants.predator import PredatorFish
from engine.inhabitants.snail import Snail

# positive test

class AquariumPositive(unittest.TestCase):
    MIN_INHABITANTS = 20
    MAX_INHABITANTS = 100
    MID_INHABITANTS = 60
        
    def test_min_inhabitants(self):
        aquarium_instance = Aquarium(AquariumPositive.MIN_INHABITANTS)
        self.assertEqual(len(aquarium_instance.inhabitants), AquariumPositive.MIN_INHABITANTS)
        Aquarium._instances.clear()
        
    def test_max_inhabitants(self):
        aquarium_instance = Aquarium(AquariumPositive.MAX_INHABITANTS)
        self.assertEqual(len(aquarium_instance.inhabitants), AquariumPositive.MAX_INHABITANTS)    
        Aquarium._instances.clear()
        
    def test_single(self):
        aquarium_1 = Aquarium(AquariumPositive.MIN_INHABITANTS)
        aquarium_2 = Aquarium(AquariumPositive.MID_INHABITANTS)
        self.assertIs(aquarium_1, aquarium_2)
        Aquarium._instances.clear()
        
    def test_weight_sanity(self):
        aquarium_instance = Aquarium(AquariumPositive.MID_INHABITANTS)
        initial_inhabitants_weight = sum(inhabitant.weight for inhabitant in aquarium_instance.inhabitants)
        aquarium_instance.evalute_inhabitants()
        finish_inhabitants_weight = sum(inhabitant.weight for inhabitant in aquarium_instance.inhabitants)
        self.assertEqual(round(initial_inhabitants_weight, 3), round(finish_inhabitants_weight, 3))

        
class PreyFishPositive(unittest.TestCase):
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 9.0
    FISH_NAME = 'Test fish'
    
    def test_min_weight(self):
        prey_fish = PreyFish(PreyFishPositive.FISH_NAME, PreyFishPositive.MIN_WEIGHT)
        self.assertEqual(prey_fish.weight, PreyFishPositive.MIN_WEIGHT)
        
    def test_max_weight(self):
        prey_fish = PreyFish(PreyFishPositive.FISH_NAME, PreyFishPositive.MAX_WEIGHT)
        self.assertEqual(prey_fish.weight, PreyFishPositive.MAX_WEIGHT)
    
    def test_fish_eat_water_plant(self):
        prey_fish = PreyFish(PreyFishPositive.FISH_NAME, PreyFishPositive.MIN_WEIGHT)
        init_fish_weight = prey_fish.weight
        plant = WaterPlant('test plant', 1.0)
        self.assertIs(prey_fish.eat(plant), plant)
        self.assertIn(plant, prey_fish.eated)
        self.assertEqual(prey_fish.weight, init_fish_weight + plant.weight)
        
    def test_fish_eat_predator(self):
        prey_fish = PreyFish(PreyFishPositive.FISH_NAME, PreyFishPositive.MIN_WEIGHT)
        init_prey_weight = prey_fish.weight
        predator_fish = PredatorFish('test predator', 10.0)
        init_predator_weight = predator_fish.weight
        
        self.assertIs(prey_fish.eat(predator_fish), prey_fish)
        self.assertNotIn(predator_fish, prey_fish.eated)
        self.assertEqual(prey_fish.weight, init_prey_weight)
        self.assertIn(prey_fish, predator_fish.eated)
        self.assertEqual(predator_fish.weight, init_predator_weight + prey_fish.weight)
        
    def test_fish_eat_fish(self):
        prey_fish = PreyFish(PreyFishPositive.FISH_NAME, PreyFishPositive.MIN_WEIGHT)
        init_fish_weight = prey_fish.weight
        other_prey_fish = PreyFish('other fish', PreyFishPositive.MAX_WEIGHT)
        self.assertIs(prey_fish.eat(other_prey_fish), None)
        self.assertNotIn(other_prey_fish, prey_fish.eated)
        self.assertEqual(prey_fish.weight, init_fish_weight)

    def test_fish_eat_snail(self):
        prey_fish = PreyFish(PreyFishPositive.FISH_NAME, PreyFishPositive.MIN_WEIGHT)
        init_fish_weight = prey_fish.weight
        snail = Snail('test snail', 1.0)
        self.assertIs(prey_fish.eat(snail), None)
        self.assertNotIn(snail, prey_fish.eated)
        self.assertEqual(prey_fish.weight, init_fish_weight)
        
        
class PredatorFishPositive(unittest.TestCase):
    WEIGHT = 10.0
    FISH_NAME = 'Test fish'
    
    def test_weight(self):
        predator_fish = PredatorFish(PredatorFishPositive.FISH_NAME, 
            PredatorFishPositive.WEIGHT)
        self.assertEqual(predator_fish.weight, PredatorFishPositive.WEIGHT)
    
    def test_predator_eat_water_plant(self):
        predator = PredatorFish(PredatorFishPositive.FISH_NAME, 
            PredatorFishPositive.WEIGHT)
        init_predator_weight = predator.weight
        plant = WaterPlant('test plant', 1.0)
        self.assertIs(predator.eat(plant), None)
        self.assertNotIn(plant, predator.eated)
        self.assertEqual(predator.weight, init_predator_weight)
        
    def test_predator_eat_predator(self):
        predator = PredatorFish(PredatorFishPositive.FISH_NAME, 
            PredatorFishPositive.WEIGHT)
        other_predator = PredatorFish('other predator', 10.0)
        init_predator_weight = predator.weight
        
        self.assertIs(predator.eat(other_predator), None)
        self.assertNotIn(other_predator, predator.eated)
        self.assertEqual(predator.weight, init_predator_weight)
        
    def test_predator_eat_fish(self):
        predator = PredatorFish(PredatorFishPositive.FISH_NAME, 
            PredatorFishPositive.WEIGHT)
        init_predator_weight = predator.weight
        prey_fish = PreyFish('test fish', 2.0)
        self.assertIs(predator.eat(prey_fish), prey_fish)
        self.assertIn(prey_fish, predator.eated)
        self.assertEqual(predator.weight, init_predator_weight + prey_fish.weight)

    def test_predator_eat_snail(self):
        predator = PredatorFish(PredatorFishPositive.FISH_NAME, 
            PredatorFishPositive.WEIGHT)
        init_predator_weight = predator.weight
        snail = Snail('test snail', 1.0)
        self.assertIs(predator.eat(snail), None)
        self.assertNotIn(snail, predator.eated)
        self.assertEqual(predator.weight, init_predator_weight)

        
class WaterPlantPositive(unittest.TestCase):
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 3.0
    PLANT_NAME = 'Test plant'
    
    def test_min_weight(self):
        plant = WaterPlant(WaterPlantPositive.PLANT_NAME, 
            WaterPlantPositive.MIN_WEIGHT)
        self.assertEqual(plant.weight, WaterPlantPositive.MIN_WEIGHT)
        
    def test_max_weight(self):
        plant = WaterPlant(WaterPlantPositive.PLANT_NAME, 
            WaterPlantPositive.MAX_WEIGHT)
        self.assertEqual(plant.weight, WaterPlantPositive.MAX_WEIGHT)
        
    def test_plant_do_not_eat_inhabitants(self):
        plant = WaterPlant(WaterPlantPositive.PLANT_NAME, 
            WaterPlantPositive.MIN_WEIGHT)
        init_plant_weight = plant.weight
        
        inhabitants = [
            WaterPlant('other plant', WaterPlantPositive.MAX_WEIGHT),
            PreyFish('test fish', 2.0),
            PredatorFish('test predator', 10.0),
            Snail('test snail', 1.0) ]
        
        [self.assertIs(plant.eat(inhabitant), None) for inhabitant in inhabitants]
        
        self.assertEqual(plant.eated, [])
        self.assertEqual(plant.weight, init_plant_weight)


class SnailPositive(unittest.TestCase):
    MIN_WEIGHT = 1.0
    MAX_WEIGHT = 5.0
    SNAIL_NAME = 'Test snail'
    
    def test_min_weight(self):
        snail = Snail(SnailPositive.SNAIL_NAME, SnailPositive.MIN_WEIGHT)
        self.assertEqual(snail.weight, WaterPlantPositive.MIN_WEIGHT)
        
    def test_max_weight(self):
        snail = Snail(SnailPositive.SNAIL_NAME, SnailPositive.MAX_WEIGHT)
        self.assertEqual(snail.weight, SnailPositive.MAX_WEIGHT)
           
    def test_snail_eat_water_plant(self):
        snail = Snail(SnailPositive.SNAIL_NAME, SnailPositive.MIN_WEIGHT)
        init_snail_weight = snail.weight
        plant = WaterPlant('test plant', 1.0)
        self.assertIs(snail.eat(plant), plant)
        self.assertIn(plant, snail.eated)
        self.assertEqual(snail.weight, init_snail_weight + plant.weight)
        
    def test_snail_eat_predator(self):
        snail = Snail(SnailPositive.SNAIL_NAME, SnailPositive.MAX_WEIGHT)
        init_snail_weight = snail.weight
        predator = PredatorFish('test predator', 10.0)
        
        self.assertIs(snail.eat(predator), None)
        self.assertNotIn(predator, snail.eated)
        self.assertEqual(snail.weight, init_snail_weight)
        
    def test_snail_eat_fish(self):
        snail = Snail(SnailPositive.SNAIL_NAME, SnailPositive.MAX_WEIGHT)
        init_snail_weight = snail.weight
        prey_fish = PreyFish('test fish', 2.0)
        self.assertIs(snail.eat(prey_fish), None)
        self.assertNotIn(prey_fish, snail.eated)
        self.assertEqual(snail.weight, init_snail_weight)

    def test_snail_eat_snail(self):
        snail = Snail(SnailPositive.SNAIL_NAME, SnailPositive.MAX_WEIGHT)
        init_snail_weight = snail.weight
        other_snail = Snail('other snail', 1.0)
        self.assertIs(snail.eat(other_snail), None)
        self.assertNotIn(other_snail, snail.eated)
        self.assertEqual(snail.weight, init_snail_weight)

  
# negative tests

class AquariumNegative(unittest.TestCase):
        
    def test_fewer_inhabitants(self):
        self.assertRaises(Exception, Aquarium, AquariumPositive.MIN_INHABITANTS - 1)
        
    def test_more_inhabitants(self):
        self.assertRaises(Exception, Aquarium, AquariumPositive.MAX_INHABITANTS + 1)
        
        
class PreyFishNegative(unittest.TestCase):
        
    def test_fewer_weight(self):
        self.assertRaises(Exception, 
            PreyFish, PreyFishPositive.FISH_NAME, PreyFishPositive.MIN_WEIGHT - 0.1)
        
    def test_greater_weight(self):
        self.assertRaises(Exception, 
            PreyFish, PreyFishPositive.FISH_NAME, PreyFishPositive.MAX_WEIGHT + 0.1)

        
class PredatorFishNegative(unittest.TestCase):
        
    def test_fewer_weight(self):
        self.assertRaises(Exception, PredatorFish, PredatorFishPositive.WEIGHT - 0.1)
        
    def test_greater_weight(self):
        self.assertRaises(Exception, PredatorFish, PredatorFishPositive.WEIGHT + 0.1)

        
class WaterPlantNegative(unittest.TestCase):
        
    def test_fewer_weight(self):
        self.assertRaises(Exception, 
            WaterPlant, WaterPlantPositive.PLANT_NAME, WaterPlantPositive.MIN_WEIGHT - 0.1)
        
    def test_greater_weight(self):
        self.assertRaises(Exception, 
            WaterPlant, WaterPlantPositive.PLANT_NAME, WaterPlantPositive.MAX_WEIGHT + 0.1)

        
class SnailNegative(unittest.TestCase):
        
    def test_fewer_weight(self):
        self.assertRaises(Exception, 
            Snail, SnailPositive.SNAIL_NAME, SnailPositive.MIN_WEIGHT - 0.1)
        
    def test_greater_weight(self):
        self.assertRaises(Exception, 
            Snail, SnailPositive.SNAIL_NAME, SnailPositive.MAX_WEIGHT + 0.1)

        
if __name__ == '__main__':
    unittest.main()
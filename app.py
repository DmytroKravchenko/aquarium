from engine.aquarium import Aquarium


if __name__ == '__main__':
    inhabitants_quantity = 90
    aquarium = Aquarium(inhabitants_quantity)
    print(aquarium)
    aquarium.evalute_inhabitants()
    print(aquarium)
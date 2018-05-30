class Inhabitant(object):
    """
    Inhabitant of the aquarium.
    """

    def __init__(self, name, weight):
        self.name = name
        self._weight = weight
        self.eaten = []

    @property
    def weight(self):
        return self._weight

    def eat(self, inhabitant):
        # can't eat self
        if self is inhabitant:
            raise Exception('Can\'t eat myself')

        self.eaten.append(inhabitant)
        self._weight += inhabitant.weight

    def __repr__(self):
        return '<{0} {1}: {2} kg>'.format(
            self.__class__.__name__, self.name, self.weight
        )

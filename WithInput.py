import queue

class Coordinate:
    def __init__(self, _min, _max):
        self.x = 0
        self.y = 0
        self.min = _min
        self.max = _max
        self.getCoordinate()

    def getValidatedCoordinate(self, _coordinate):
        error = 'Coordinates must be between ' + str(self.min) + " and " + str(self.max)
        while True:
            try:
                c = int(input('Enter ' + _coordinate + " coordinate (" + str(self.min) + "-" + str(self.max - 1) + ") - "))
                if self.min <= c < self.max:
                    return c
                else:
                    print(error)
            except:
                print(error)

    def getCoordinate(self):
        return self.getValidatedCoordinate('x'), self.getValidatedCoordinate('y')

    #def getCoordinate(self, _coordinate):
    #    return _coordinate.x, _coordinate.y


class Zombie:
    count = 0
    def __init__(self, _movementPattern, _grid):
        self.zombieId = Zombie.count
        Zombie.count = Zombie.count + 1
        print('Enter zombie coordinates - ')
        self.coordinates = Coordinate(_grid.min, _grid.max)
        self.movementPattern = _movementPattern
    def move(self):
        locations = []
        self.coordinates, locations = self.movementPattern.move(self.coordinates)
        return locations

class Creature:
    count = 0
    def __init__(self, _grid):
        print('Enter creature ' + str(Creature.count) + ' coordinates.')
        Creature.count = Creature.count + 1
        self.coordinate = Coordinate(0, _grid.max)
    def isZmobieInfectingCreature(self, _c):
        if self.coordinate.x == _c.x and self.coordinate.y == _c.y:
            return True
        return False

class movementPattern:
    def __init__(self, _grid):
        #exception handling for pattern
        self.pattern = input("Enter zombie movement pattern string which is combination of letter 'U' (up), 'D' (down), 'L' (left) and 'R' (right). e.g. UUR, RUL - ")
        self.maxLimit = _grid.max
    def move(self, _start):
        print('Moving')
        touchPoints = []
        for movement in self.pattern:
            if movement == 'R':
                _start.x = (_start.x + 1) % self.maxLimit
            if movement == 'L':
                _start.x = (_start.x - 1) % self.maxLimit
            if movement == 'U':
                _start.y = (_start.y - 1) % self.maxLimit
            if movement == 'D':
                _start.y = (_start.y + 1) % self.maxLimit
            touchPoints.insert(_start)
        return _start, touchPoints


class Grid:
    def __init__(self):
        self.N = int(input("Enter grid dimension - "))      # exception handling for non int
        self.min = 0
        self.max = self.N - 1


class zombieLand:

    def __init__(self):
        self.zombieQueue = queue.Queue()
        self.creature = []
        self.grid = Grid()
        self.zombieQueue.put( Zombie ( movementPattern(self.grid), self.grid ) )
        creatureCount = int(input("Enter creature count - "))
        for x in range(0, creatureCount):
            self.creature.append( Creature(self.grid) )

    def run(self):
        print ('running')



z = zombieLand()


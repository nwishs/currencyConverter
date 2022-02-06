import queue
import copy

class Coordinate:
    def __init__(self, _x, _y, _grid):
        self.x = _x
        self.y = _y
        self.min = _grid.min
        self.max = _grid.max
        try:
            self.validateCoordinate(self.x)
            self.validateCoordinate(self.y)
        except:
            raise ValueError('Error while parsing and validating coordinates')

    def validateCoordinate(self, _c):
        error1 = 'Coordinates must be between ' + str(self.min) + " and " + str(self.max)
        error2 = 'Type error'
        while True:
            try:
                if self.min <= int(_c) <= self.max:
                    return _c
                else:
                    raise ValueError(error1)
            except:
                raise TypeError(error2)

    def display(self):
        return ('(' + str(self.x) + ',' + str(self.y) + ')')



class Zombie:
    count = 0
    def __init__(self, _movementPattern, _grid, _coordinate):
        self.zombieId = Zombie.count
        Zombie.count = Zombie.count + 1
        self.coordinate = _coordinate
        self.movementPattern = _movementPattern
        self.dormant = False
    def move(self):
        moved, self.dormant, self.coordinate = self.movementPattern.move(self.coordinate, self.zombieId)
        if moved == True:
            print("Zombie " + str(self.zombieId) + " moved to " + self.coordinate.display())
        return self.coordinate

class Creature:
    count = 0
    def __init__(self, _grid, _coordinate):
        Creature.count = Creature.count + 1
        self.coordinate = _coordinate
        self.isZombie = False

    def isCreatureGettingInfected(self, _c, _zombie):
        if self.coordinate.x == _c.x and self.coordinate.y == _c.y and self.isZombie == False:
            self.isZombie = True
            print("zombie " + str(_zombie.zombieId) + " infected creature at " + _c.display())
            return True
        return False

class MovementPattern:
    def __init__(self, _grid, _pattern):
        #exception handling for pattern
        self.pattern = _pattern
        self.grid = _grid
        self.nextMoveIndex = 0
        self.patternComplete = False
        if self.validatePattern() == False:
            raise ValueError(_pattern + ' is not a valid pattern')

    def validatePattern(self):
        return True

    def move(self, _start, _id):
        moved = False
        if self.patternComplete == True:
            return moved, self.patternComplete, _start
        nextMovement = self.pattern[self.nextMoveIndex]
        if nextMovement == 'R':
            _start.x = (_start.x + 1) % self.grid.n
        if nextMovement == 'L':
            _start.x = (_start.x - 1) % self.grid.n
        if nextMovement == 'U':
            _start.y = (_start.y - 1) % self.grid.n
        if nextMovement == 'D':
            _start.y = (_start.y + 1) % self.grid.n
        self.nextMoveIndex += 1
        moved = True
        if self.nextMoveIndex == len(self.pattern):
            self.patternComplete = True
        return moved, self.patternComplete, _start


class Grid:
    def __init__(self, _n):
        self.n = _n
        self.min = 0
        self.max = self.n - 1


class zombieLand:

    def __init__(self, _n, _zombieCoordinates, _creatureCoordinateList, _pattern):
        self.zombieQueue = queue.Queue()
        self.dormantZombies = queue.Queue()
        self.creature = []
        self.grid = Grid(_n)
        self.pattern = _pattern
        self.zombieQueue.put(Zombie(MovementPattern(self.grid, self.pattern), self.grid, Coordinate(_zombieCoordinates[0], _zombieCoordinates[1], self.grid)))
        for c in _creatureCoordinateList:
            self.creature.append(Creature(self.grid, Coordinate(c[0], c[1], self.grid)))

    def run(self):
        while self.zombieQueue.empty() == False:
            z = self.zombieQueue.get()
            while z.dormant == False:
                touchPoint = z.move()
                for c in self.creature:
                    if c.isCreatureGettingInfected(touchPoint, z):
                        self.zombieQueue.put(Zombie(MovementPattern(self.grid, self.pattern), self.grid, copy.copy(touchPoint)))
            self.dormantZombies.put(z)

    def printAllZombiePosition(self):
        print('Zombies\' position:')
        while self.dormantZombies.empty() == False:
            z = self.dormantZombies.get()
            print(z.coordinate.display())

    def printAllCreaturePosition(self):
        print('Creatures\' position:')
        for c in self.creature:
            if c.isZombie == False:
                print(c.coordinate.display())



N = 4
zombieCoordinate = (0,0)
creatureCoordinateList = [(0,0)]
pattern = 'RR'

z = zombieLand(N, zombieCoordinate, creatureCoordinateList, pattern)
z.run()
z.printAllZombiePosition()
z.printAllCreaturePosition()

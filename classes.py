import random
class Room(object):
    rooms = []
    selectionRooms = []
    numOfRooms = 10
    rows = 11
    cols = 11
    def __init__(self, cell):
        self.cell = cell
        self.hasPlayer = False
        self.player = None
        self.playerAttacks = []

    def __repr__(self):
        return f'Room({self.cell}, Spawn:{self.cell == (5,5)}, HasPlayer:{self.hasPlayer}, Player:{self.player})'

    def __eq__(self, other):
        return (isinstance(other, Room) and (self.cell == other.cell and self.hasPlayer == other.hasPlayer))

    def generateRooms(self):
        startingRoom = Room((Room.rows//2, Room.cols//2))
        startingRoom.hasPlayer = True
        Room.rooms.append(startingRoom)
        for i in range(Room.numOfRooms):
            roomRow, roomCol = Room.rooms[i].cell
            for drow, dcol in [(-1, 0), (0, +1), (+1, 0), (0, -1)]:
                newRow, newCol = roomRow + drow, roomCol + dcol
                if (Room((newRow, newCol)) not in Room.selectionRooms and 
                    Room((newRow, newCol)) not in Room.rooms and
                    newRow < Room.rows and newCol < Room.cols):
                    Room.selectionRooms.append(Room((newRow, newCol)))
            randomRoom = random.choice(Room.selectionRooms)
            Room.rooms.append(randomRoom)
            Room.selectionRooms.remove(randomRoom)
        return Room.rooms


class Player(object):
    def __init__(self, appWidth, appHeight): 
        self.cx = appWidth//2
        self.cy = appHeight//2
        self.speed = 10
        self.width = 20
        self.health = 5
    
    def __repr__(self):
        return f'Player(Location:{(self.cx, self.cy)}, Health:{self.health})'

    def attack(self, x, y):
        radius = 8
        startX, startY = self.cx, self.cy
        deltaX, deltaY = self.findAttackDeltas(x, y, startX, startY)
        return [startX, startY, radius, deltaX, deltaY]

    def findAttackDeltas(self, x, y, cx, cy):
        deltaX = 0
        deltaY = 0
        speed = 15
        #right:
        if x >= cx and x >= abs(y):
            deltaX = speed
        #left
        elif x <= cx and y >= x:
            deltaX = -speed
        #Up
        elif y <= cy and x >= abs(y):
            deltaY = -speed
        #Down
        elif y >= cy and y >= abs(x):
            deltaY = speed
        return (deltaX, deltaY)

class Monster(object):
    def __init__(self):
        pass

class Spritesheet(object):
    def __init__(self):
        pass
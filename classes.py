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
        self.monsters = []

    def __repr__(self):
        return f'Room({self.cell}, HasPlayer:{self.hasPlayer}, Player:{self.player}, Monsters:{len(self.monsters)})'

    def __eq__(self, other):
        return (isinstance(other, Room) and (self.cell == other.cell and self.hasPlayer == other.hasPlayer))

    # https://youtu.be/tUskxXXTh7s?t=59
    #This function was influenced by the video above.
    #The idea of taking a grid placing a cell in the middle then putting 
    #all adjacent cells into a list and then randomly selecting from that list 
    #of adjacent cells to use as the next room, and then repeating until there is 
    #a list that is the size of the number of rooms that you want was taken from
    #this video. No code was taken from the video only concepts. 
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

    def generateMonster(self, monster):
        self.monsters.append(monster)

class Player(object):
    def __init__(self, appWidth, appHeight): 
        self.cx = appWidth//2
        self.cy = appHeight//2
        self.movementSpeed = 10
        self.width = 20
        self.health = 6
        self.attackSpeed = 15
    
    def __repr__(self):
        return f'Player(Location:{(self.cx, self.cy)}, Health:{self.health})'

    def attack(self, x, y):
        radius = 8
        cx, cy = self.cx, self.cy
        deltaX, deltaY = self.findAttackDeltas(x, y, cx, cy)
        return [cx, cy, radius, deltaX, deltaY]

#The math for this is not right, needs to be fixed
    def findAttackDeltas(self, x, y, cx, cy):
        deltaX = 0
        deltaY = 0
        #right:
        if x >= cx and x >= abs(y):
            deltaX = self.attackSpeed
        #left
        elif x <= cx and y >= x:
            deltaX = -self.attackSpeed
        #Up
        elif y <= cy and x >= abs(y):
            deltaY = -self.attackSpeed
        #Down
        elif y >= cy and y >= abs(x):
            deltaY = self.attackSpeed
        return (deltaX, deltaY)

class Monster(object):
    def __init__(self, appWidth, appHeight):
        self.width = 20
        self.cx = random.randint(self.width, appWidth)
        self.cy = random.randint(self.width, appHeight)
        self.speed = 5
        self.health = 5

    def __repr__(self):
        return f'Monster(Location:{(self.cx, self.cy)}, Health:{self.health})'


class Spritesheet(object):
    def __init__(self):
        pass
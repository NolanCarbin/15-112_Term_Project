import random
from monsters import *

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

    ##############
    #Room Methods
    ##############

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

    @staticmethod
    def createRoomPixelList(canvasWidth, canvasHeight):
        rows = canvasWidth // 40
        cols = canvasHeight // 40
        result = []
        for row in range(rows):
            for col in range(cols):
                result.append(((row * 40), (col * 40)))
        return result

    #interval for using a the pixel graph is 10
    #interval for using cells is 1
    @staticmethod
    def createAdjacencyList(L, interval):
        def isConnected(x0, y0, x1, y1, interval):
            return ((abs(x0 - x1) == 0 and abs(y0 - y1) == interval) or 
            (abs(x0 - x1) == interval and abs(y0 - y1) == 0))

        graph = dict()
        for nodeRow, nodeCol in L:
            graph[(nodeRow, nodeCol)] = set()
            for edgeRow, edgeCol in L:
                if (nodeRow, nodeCol) != (edgeRow, edgeCol):
                    if isConnected(nodeRow, nodeCol, edgeRow, edgeCol, interval):
                        graph[(nodeRow, nodeCol)].add((edgeRow, edgeCol))        
        return graph


    def generateMonster(self, graph, appWidth, appHeight):
        cx = random.randint(20, appWidth - 20)
        cy = random.randint(20, appHeight - 20)
        while (cx, cy) not in graph:
            cx = random.randint(20, appWidth - 20)
            cy = random.randint(20, appHeight - 20)
        monster = Monster(cx, cy)
        self.monsters.append(monster)
  
################
#Functions
################

def checkIfChangeOfRoom(app):
    #checks if all monsters in the room are dead
    if len(app.currentRoom.monsters) == 0:
        #left door
        if inBoundsOfDoor(app, 'left') and checkIfAdjacentRoom(app, (0,-1)):
            newRoomCell = (app.currentRoom.cell[0] + (0), app.currentRoom.cell[1] + (-1))
            changeRoom(app, newRoomCell, (0,-1))
        #right door
        elif inBoundsOfDoor(app, 'right') and checkIfAdjacentRoom(app, (0,+1)):
            newRoomCell = (app.currentRoom.cell[0] + (0), app.currentRoom.cell[1] + (+1))
            changeRoom(app, newRoomCell, (0,+1))
        #top door
        elif inBoundsOfDoor(app, 'top') and checkIfAdjacentRoom(app, (-1,0)):
            newRoomCell = (app.currentRoom.cell[0] + (-1), app.currentRoom.cell[1] + (0))
            changeRoom(app, newRoomCell, (-1,0))
        #bottom door
        elif inBoundsOfDoor(app, 'bottom') and checkIfAdjacentRoom(app, (+1,0)):
            newRoomCell = (app.currentRoom.cell[0] + (+1), app.currentRoom.cell[1] + (0))
            changeRoom(app, newRoomCell, (+1,0))


def inBoundsOfRoom(app):
    player = app.player
    if player.cx - player.width < 0:
        player.cx = player.width
    elif player.cx + player.width > app.width:
        player.cx = app.width - player.width
    elif player.cy - player.width < 0:
        player.cy = player.width
    elif player.cy + player.width > app.height:
        player.cy = app.height - player.width

def inBoundsOfDoor(app, door):
    doorList = app.doors[door]
    x0, y0, x1, y1 = doorList[0], doorList[1], doorList[2], doorList[3] 
    return (app.player.cx - app.player.width <= x1 and 
            app.player.cx + app.player.width >= x0 and 
            app.player.cy - app.player.width <= y1 and 
            app.player.cy + app.player.width >= y0)
        
def checkIfAdjacentRoom(app, adjacentCellDirection):
    drow, dcol = adjacentCellDirection
    roomRow, roomCol = app.currentRoom.cell
    newCell = (roomRow + drow, roomCol + dcol)
    for room in app.rooms:
        if room.cell == newCell:
            return True
    return False

def changeRoom(app, newRoomCell, direction):
    app.currentRoom.hasPlayer = False
    for room in app.rooms:
        if room.player != None:
            room.player = None
        if room.cell == newRoomCell:
            room.hasPlayer = True
            room.player = app.player
            app.currentRoom = room
            newPlayerPosition(app, direction)
            print(app.currentRoom)

def newPlayerPosition(app, direction):
    if direction == (0,-1):
        app.player.cx = app.width - app.doorWidth
        app.player.cy = app.height//2
    elif direction == (0,+1):
        app.player.cx = app.doorWidth
        app.player.cy = app.height//2
    elif direction == (-1,0):
        app.player.cx = app.width//2
        app.player.cy = app.height - app.doorWidth
    elif direction == (+1,0):
        app.player.cx = app.width//2
        app.player.cy = app.doorWidth
import random
from monsters import *

#Room class 
#Contains room specific methods that alter the room object

class Room(object):
    rooms = []
    selectionRooms = []
    numOfRooms = 10
    rows = 11
    cols = 11
    floorNumber = 0
    def __init__(self, cell):
        self.cell = cell
        self.hasPlayer = False
        self.isBossRoom = False
        self.bossRoomDoorWidth = 30
        self.player = None
        self.playerAttacks = []
        self.monsters = [] 
        self.bossAttacks = []
        self.rocks = []
        self.rockWidth = 20
        self.graph = {}
        self.items = []

    def __repr__(self):
        return f'''Room({self.cell}, HasPlayer:{self.hasPlayer}, 
        isBossRoom:{self.isBossRoom}, Player:{self.player}, 
        Monsters:{len(self.monsters)})'''

    def __eq__(self, other):
        return (isinstance(other, Room) and (self.cell == other.cell))

    ##############
    #Room Methods
    ##############

    # https://youtu.be/tUskxXXTh7s?t=59
    #This function was influenced by the video above.
    #The idea of taking a grid placing a cell in the middle then putting 
    #all adjacent cells into a list and then randomly selecting from that list 
    #of adjacent cells to use as the next room, and then repeating until there 
    #is a list that is the size of the number of rooms that you want was taken 
    #from this video. No code was taken from the video, only concepts. 
    def generateRooms(self):
        startingRoom = Room((0,0))
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

    def generateMonster(self, graph, appWidth, appHeight):
        cx = random.randint(40, appWidth - 40)
        cy = random.randint(40, appHeight - 40)
        while (cx, cy) not in graph:
            cx = random.randint(40, appWidth - 40)
            cy = random.randint(40, appHeight - 40)
        monsters = [Monster(cx,cy),BatMonster(cx,cy)]
        monster = random.choice(monsters)
        self.monsters.append(monster)

    def generateBoss(self, graph, appWidth, appHeight):
        cx = random.randint(40, appWidth - 40)
        cy = random.randint(40, appHeight - 40)
        while (cx, cy) not in graph:
            cx = random.randint(40, appWidth - 40)
            cy = random.randint(40, appHeight - 40)
        boss = BossMonster(cx, cy)
        self.monsters.append(boss)

    @staticmethod
    def createRoomPixelList(canvasWidth, canvasHeight):
        rows = canvasWidth // 40
        cols = canvasHeight // 40
        result = []
        for row in range(1,rows):
            for col in range(1,cols):
                result.append(((row * 40), (col * 40)))
        return result

    #interval for using a the pixel graph is 40
    #interval for using room cells is 1
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

    @staticmethod
    def createRoomList():
        roomCellList = []
        for room in Room.rooms:
            roomCellList.append(room.cell)
        return roomCellList

    #findFarthestRoom() uses BFS to search every path in the app.rooms list
    #it returns the last cell that the algorithm reaches. Which is the farthest 
    #cell from the startingCell. The BFS algorithm is taken from this site:
    #https://www.redblobgames.com/pathfinding/a-star/introduction.html

    @staticmethod
    def findFarthestRoom(graph, startingCell):
        queue = Queue()
        reached = set()
        queue.enqueue(startingCell) 
        reached.add(startingCell)
        while queue.len() != 0:
            currentNode = queue.dequeue()
            for nextNode in graph[currentNode]:
                if nextNode not in reached:
                    queue.enqueue(nextNode)
                    reached.add(currentNode) 
            if queue.len() == 1:
                return (queue.queue[0])


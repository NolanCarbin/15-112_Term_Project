from cmu_112_graphics import *
from classes import *

def appStarted(app):
    app.rooms = Room.generateRooms(Room)
    app.player = Player(app.width, app.height)
    for room in app.rooms:
        if room.hasPlayer:
            app.currentRoom = room
    app.doorWidth = 40
    app.doors = {
        'top':[app.width//2 - app.doorWidth, 0, app.width//2 + app.doorWidth, app.doorWidth//3], 
        'bottom':[app.width//2 - app.doorWidth, app.height - app.doorWidth//3, app.width//2 + app.doorWidth, app.height],
        'left':[0, app.height//2 - app.doorWidth, app.doorWidth//3, app.height//2 + app.doorWidth],
        'right':[app.width - app.doorWidth//3, app.height//2 - app.doorWidth, app.width, app.height//2 + app.doorWidth]
    }


def keyPressed(app, event):
    playerMovement(app, event, app.player)

def playerMovement(app, event, player):
    if event.key in ['w', 'Up']:
        player.cy -= player.delta
    elif event.key in ['s', 'Down']:
        player.cy += player.delta
    elif event.key in ['a', 'Left']:
        player.cx -= player.delta
    elif event.key in ['d', 'Right']:
        player.cx += player.delta
    checkIfChangeOfRoom(app)
    inBoundsOfRoom(app)

def timerFired(app):
    pass
        

def checkIfChangeOfRoom(app):
    player = app.player
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
    #adjacentCellDirection == tuple #ex:(0,-1),(0,+1),(+1,0),(-1,0)
    # return True or False
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
        if room.cell == newRoomCell:
            room.hasPlayer = True
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

def redrawAll(app, canvas):
    for room in app.rooms:
        if room.hasPlayer: 
            drawRoom(app, canvas, room)
    drawPlayer(app, canvas, app.player)

def drawPlayer(app, canvas, player):
    canvas.create_rectangle(player.cx - player.width, 
    player.cy - player.width, player.cx + player.width, player.cy + player.width)

def drawRoom(app, canvas, room):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='grey')
    # canvas.create_rectangle(2,2, app.width - 2, app.height - 2, width=5)
    drawDoors(app, canvas)

def drawDoors(app, canvas):
    dirs = [(0,-1),(0,+1),(-1,0),(+1,0)]
    for drow, dcol in dirs:
        if checkIfAdjacentRoom(app, (drow,dcol)):
            if drow == -1: #top door
                canvas.create_rectangle(app.doors['top'][0], app.doors['top'][1], app.doors['top'][2], app.doors['top'][3])
            elif drow == +1: #bottom door
                canvas.create_rectangle(app.doors['bottom'][0], app.doors['bottom'][1], app.doors['bottom'][2], app.doors['bottom'][3])
            elif dcol == -1: #left door
                canvas.create_rectangle(app.doors['left'][0], app.doors['left'][1], app.doors['left'][2], app.doors['left'][3])
            elif dcol == +1: #right door
                canvas.create_rectangle(app.doors['right'][0], app.doors['right'][1], app.doors['right'][2], app.doors['right'][3])



runApp(width=800, height=600)
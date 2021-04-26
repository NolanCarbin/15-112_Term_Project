from cmu_112_graphics import *
from classes import *

def appStarted(app):
    app.rooms = Room.generateRooms(Room)
    for room in app.rooms:
        if room.hasPlayer:
            app.player = room.player = Player(app.width, app.height)
            app.currentRoom = room
    app.doorWidth = 40
    app.doors = {
        'top':[app.width//2 - app.doorWidth, 0, app.width//2 + app.doorWidth, app.doorWidth//3], 
        'bottom':[app.width//2 - app.doorWidth, app.height - app.doorWidth//3, app.width//2 + app.doorWidth, app.height],
        'left':[0, app.height//2 - app.doorWidth, app.doorWidth//3, app.height//2 + app.doorWidth],
        'right':[app.width - app.doorWidth//3, app.height//2 - app.doorWidth, app.width, app.height//2 + app.doorWidth]
    }

def mousePressed(app, event):
    app.currentRoom.playerAttacks.append(app.player.attack(event.x, event.y))

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    playerMovement(app, event)

def playerMovement(app, event):
    if event.key in ['w', 'Up']:
        app.player.cy -= app.player.speed
        app.player.facingDirection = 'U'
    elif event.key in ['s', 'Down']:
        app.player.cy += app.player.speed
        app.player.facingDirection = 'D'
    elif event.key in ['a', 'Left']:
        app.player.cx -= app.player.speed
        app.player.facingDirection = 'L'
    elif event.key in ['d', 'Right']:
        app.player.cx += app.player.speed
        app.player.facingDirection = 'R'
    checkIfChangeOfRoom(app)
    inBoundsOfRoom(app)

def timerFired(app):
    if len(app.currentRoom.playerAttacks) > 0:
        movePlayerAttacks(app)

def movePlayerAttacks(app):
    for attack in app.currentRoom.playerAttacks: 
        deltaX = attack[3]
        deltaY = attack[4]
        #circle x:
        attack[0] += deltaX
        #circle y:
        attack[1] += deltaY
        #check if not inBoundsOfRoom:
        if (attack[0] < 0 or attack[0] > app.width or 
            attack[1] < 0 or attack[1] > app.height): 
            app.currentRoom.playerAttacks.remove(attack)
        #check if inBoundsOfMonsters: 
        #   app.player.attacks.remove(attack)
        
def checkIfChangeOfRoom(app):
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

def redrawAll(app, canvas):
    for room in app.rooms:
        if room.hasPlayer: 
            drawRoom(app, canvas, room)
            drawPlayer(app, canvas)
            drawPlayerAttacks(app, canvas)

def drawPlayer(app, canvas):
    player = app.player
    canvas.create_rectangle(player.cx - player.width, 
    player.cy - player.width, player.cx + player.width, player.cy + player.width)

def drawPlayerAttacks(app, canvas):
    for attack in app.currentRoom.playerAttacks:
        cx = attack[0]
        cy = attack[1]
        r = attack[2]
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='white')

def drawRoom(app, canvas, room):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='light grey')
    drawDoors(app, canvas)

#make doors resizable to the window in the future
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
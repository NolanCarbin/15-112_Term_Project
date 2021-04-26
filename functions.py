import math, random, string

def playerMovement(app, event):
    if event.key in ['w', 'Up']:
        app.player.cy -= app.player.movementSpeed
        app.player.facingDirection = 'U'
    elif event.key in ['s', 'Down']:
        app.player.cy += app.player.movementSpeed
        app.player.facingDirection = 'D'
    elif event.key in ['a', 'Left']:
        app.player.cx -= app.player.movementSpeed
        app.player.facingDirection = 'L'
    elif event.key in ['d', 'Right']:
        app.player.cx += app.player.movementSpeed
        app.player.facingDirection = 'R'
    checkIfChangeOfRoom(app)
    inBoundsOfRoom(app)

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
        for monster in app.currentRoom.monsters:
            if attackInBoundsOfMonster(attack[0], attack[1], attack[2], monster.cx, monster.cy, monster.width): 
                app.currentRoom.playerAttacks.remove(attack)                
                monster.health -= 1
                if monster.health == 0:
                    app.currentRoom.monsters.remove(monster)

def monsterAttack(app):
    if len(app.currentRoom.monsters) == 0: return 
    for monster in app.currentRoom.monsters:
        if(app.player.cx - app.player.width <= monster.cx + monster.width and app.player.cx + app.player.width >= monster.cx - monster.width and app.player.cy - app.player.width <= monster.cy + monster.width and app.player.cy + app.player.width >= monster.cy - monster.width):    app.player.health -= 1

#taken from: http://www.jeffreythompson.org/collision-detection/circle-rect.php converted from another language to python 
def attackInBoundsOfMonster(cx, cy, r, rx, ry, width):
    testX = cx
    testY = cy
    if (cx < rx):        
        testX = rx
    elif (cx > rx + width):
        testX = rx + width
    if (cy < ry):
        testY = ry
    elif (cy > ry + width):
        testY = ry + width
#get distance from closest edges
    distX = cx-testX
    distY = cy-testY
    distance = math.sqrt((distX * distX) + (distY * distY))
#if the distance is less than the radius, then collision
    if (distance <= r):
        return True
    return False

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
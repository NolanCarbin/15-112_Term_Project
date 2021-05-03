class Player(object):
    def __init__(self, appWidth, appHeight): 
        self.cx = appWidth//2
        self.cy = appHeight//2
        self.movementSpeed = 10
        self.width = 20
        self.health = 12
        self.attackSpeed = 15
    
    def __repr__(self):
        return f'Player(Location:{(self.cx, self.cy)}, Health:{self.health})'

    def attackWithMouse(self, app, x, y):
        ##########
        app.wizard.attackingCounter = 0
        app.wizard.attacking = True
        ##########
        radius = 8
        cx, cy = self.cx, self.cy
        deltaX = (x - cx) / self.attackSpeed
        deltaY = (y - cy) / self.attackSpeed
        app.currentRoom.playerAttacks.append({'cx': cx, 'cy': cy, 'radius': radius, 'deltaX': deltaX, 'deltaY':deltaY})

    def attackWithKeys(self, app, key):
        if key not in ['Right', 'Left', 'Up', 'Down']: return 
        #############
        app.wizard.attackingCounter = 0
        app.wizard.attacking = True
        #############
        radius = 8
        cx, cy = self.cx, self.cy
        deltaX = 0
        deltaY = 0
        if key == 'Right':
            deltaX = self.attackSpeed
        elif key == 'Left':
            deltaX = -self.attackSpeed
        elif key == 'Up':
            deltaY = -self.attackSpeed
        elif key == 'Down':
            deltaY = self.attackSpeed
        app.currentRoom.playerAttacks.append({'cx': cx, 'cy': cy, 'radius': radius, 'deltaX': deltaX, 'deltaY':deltaY})

    #taken from: https://www.geeksforgeeks.org/check-if-any-point-overlaps-the-given-circle-and-rectangle/
    #modified to be a method and fit the needs of my app
    def attackInBoundsOfPlayer(self, circleX, circleY, r): 
        x1, y1 = self.cx - self.width, self.cy - self.width
        x2, y2 = self.cx + self.width, self.cy + self.width
        #(xn, yn) is the nearest point 
        xn = max(x1, min(circleX, x2))
        yn = max(y1, min(circleY, y2))
        #(dx, dy) is the distance between the nearest point and the center of 
        #the circle
        dx = xn - circleX
        dy = yn - circleY
        return (dx**2 + dy**2) <= r**2

    
def playerMovement(app, key):
    if key == 'w':
        app.player.cy -= app.player.movementSpeed
        if inBoundsOfRocks(app): app.player.cy += app.player.movementSpeed
        app.wizard.isRunning = True
    elif key == 's':
        app.player.cy += app.player.movementSpeed
        if inBoundsOfRocks(app): app.player.cy -= app.player.movementSpeed
        app.wizard.isRunning = True
    elif key in {'a', 'Left'}:
        if key == 'a':
            app.player.cx -= app.player.movementSpeed
            if inBoundsOfRocks(app): app.player.cx += app.player.movementSpeed
        app.wizard.isRunning = True
        if not app.wizard.flipped:
            app.wizard.flipped = True
            app.wizard.flipSpriteSheet(app.wizard.runningSprites)
            app.wizard.flipSpriteSheet(app.wizard.attackSprites)
            app.wizard.flipSpriteSheet(app.wizard.idleSprites)
    elif key in {'d', 'Right'}:
        if key == 'd': 
            app.player.cx += app.player.movementSpeed
            if inBoundsOfRocks(app): app.player.cx -= app.player.movementSpeed
        app.wizard.isRunning = True
        if app.wizard.flipped:
            app.wizard.flipped = False
            app.wizard.flipSpriteSheet(app.wizard.runningSprites)
            app.wizard.flipSpriteSheet(app.wizard.attackSprites)
            app.wizard.flipSpriteSheet(app.wizard.idleSprites)

    checkIfChangeOfRoom(app)
    inBoundsOfRoom(app)
    inBoundsOfRocks(app)

def movePlayerAttacks(app):
    for attack in app.currentRoom.playerAttacks: 
        attack['cx'] = attack['cx'] + attack['deltaX']
        attack['cy'] = attack['cy'] + attack['deltaY']
        #check if not inBoundsOfRoom:
        if (attack['cx'] < 0 or attack['cx'] > app.width or 
            attack['cy'] < 0 or attack['cy'] > app.height): 
            app.currentRoom.playerAttacks.remove(attack)
        #check if inBoundsOfMonsters:
        for monster in app.currentRoom.monsters:
            if monster.attackInBoundsOfMonster(attack['cx'], attack['cy'], attack['radius']):
                if attack in app.currentRoom.playerAttacks:
                    app.currentRoom.playerAttacks.remove(attack)                
                    monster.health -= 1
                if monster.health == 0:
                    app.currentRoom.monsters.remove(monster)

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


def inBoundsOfDoor(app, door):
    doorList = app.doors[door]
    x0, y0, x1, y1 = doorList[0], doorList[1], doorList[2], doorList[3] 
    return (app.player.cx - app.player.width <= x1 and 
            app.player.cx + app.player.width >= x0 and 
            app.player.cy - app.player.width <= y1 and 
            app.player.cy + app.player.width >= y0)

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

def inBoundsOfRocks(app):
    player = app.player
    rockWidth = app.currentRoom.rockWidth
    for rockX, rockY in app.currentRoom.rocks:
        if (player.cx - player.width < rockX + rockWidth and 
            player.cx + player.width > rockX - rockWidth and 
            player.cy - player.width < rockY + rockWidth and 
            player.cy + player.width > rockY - rockWidth):
            return True
    return False

    
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

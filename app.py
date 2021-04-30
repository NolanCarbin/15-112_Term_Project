from cmu_112_graphics import *
from monsters import *
from player import * 
from rooms import *
import random, time

#############
#Main App
#############

def appStarted(app):
    app.graph = Room.createAdjacencyList(Room.createRoomPixelList(app.width, app.height), 40)
    app.rooms = Room.generateRooms(Room)
    app.roomGraph = Room.createAdjacencyList(Room.createRoomList(), 1)
    #sets up player:
    for room in app.rooms:
        if room.hasPlayer:
            app.player = room.player = Player(app.width, app.height)
            app.currentRoom = room
    farthestRoomCell = Room.findFarthestRoom(app.roomGraph, app.currentRoom.cell)
    #sets up monsters and boss:
    for room in app.rooms:
        if room.cell == farthestRoomCell:
            app.bossRoom = room
            room.isBossRoom = True
            room.generateBoss(app.graph, app.width, app.height)
        if room.cell != (5,5) and room.cell != farthestRoomCell:
            for i in range(random.randint(2,5)):
                room.generateMonster(app.graph, app.width, app.height)
        
    app.doorWidth = 40
    app.doors = {
        'top':[app.width//2 - app.doorWidth, 0, app.width//2 + app.doorWidth, app.doorWidth//3], 
        'bottom':[app.width//2 - app.doorWidth, app.height - app.doorWidth//3, app.width//2 + app.doorWidth, app.height],
        'left':[0, app.height//2 - app.doorWidth, app.doorWidth//3, app.height//2 + app.doorWidth],
        'right':[app.width - app.doorWidth//3, app.height//2 - app.doorWidth, app.width, app.height//2 + app.doorWidth]
    }
    app.gameOver = False
    ##################
    app.keyPressedTimer = None
    app.totalKeyPressedTimer = None
    app.lastKeyPressed = None
    ##################
    app.monsterMovementTimer = 0
    app.monsterAttackTimer = 0
    app.bossAttackTimer = 0
    print(app.currentRoom)
    
def mousePressed(app, event):
    app.player.attackWithMouse(app, event.x, event.y)

def keyPressed(app, event):
    #Used for the os delay:
    ###################
    app.keyPressedTimer = time.time()
    app.totalKeyPressedTimer = time.time()
    app.lastKeyPressed = event.key
    ###################
    if event.key == 'r':
        Room.rooms = []
        Room.selectionRooms = []
        appStarted(app)
    playerMovement(app, event.key)
    app.player.attackWithKeys(app, event.key)
    if event.key == 'b':
        app.currentRoom.hasPlayer = False
        app.currentRoom.player = None
        app.currentRoom = app.bossRoom 
        app.currentRoom.hasPlayer = True
        app.currentRoom.player = app.player

def keyReleased(app, event):
    app.keyPressedTimer = None
    app.totalKeyPressedTimer = None
    app.lastKeyPressed = None

def timerFired(app):
    #Used for the os delay:
    ##################
    if app.keyPressedTimer != None and time.time() - app.keyPressedTimer >= 0.02:
        playerMovement(app, app.lastKeyPressed) 
        app.keyPressedTimer = time.time() #reset the timer
    #Lets the OS repeat the function call
    if app.totalKeyPressedTimer != None and time.time() - app.totalKeyPressedTimer >= 0.5: 
        app.keyPressedTimer = None
        app.totalKeyPressedTimer = None
    # ##################
    if len(app.currentRoom.playerAttacks) > 0:
        movePlayerAttacks(app)
    if len(app.currentRoom.bossAttacks) > 0:
        BossMonster.moveBossAttacks(app)
    ###################
    if app.player.health <= 0:
        app.gameOver = True
    ###################
    app.monsterMovementTimer += 1
    app.monsterAttackTimer += 1
    app.bossAttackTimer += 1
    for monster in app.currentRoom.monsters:
        if len(app.currentRoom.monsters) == 0: return 
        if app.monsterMovementTimer % monster.movementSpeed == 0:
            monster.moveTowardPlayer(app)
        if app.monsterMovementTimer % monster.attackSpeed == 0:
            monster.inBoundsOfPlayer(app)
        if app.currentRoom == app.bossRoom:
            if app.bossAttackTimer % monster.shootingSpeed == 0:
                monster.attackPlayer(app)
    ###################
    # if len(app.bossRoom.monsters) == 0 and if app.player is in bounds of door)
    ###################

def redrawAll(app, canvas):
    if app.gameOver:
        drawGameOver(app, canvas)
    else:
        drawRoom(app, canvas)
        drawDoorToNextFloor(app, canvas)
        drawPlayer(app, canvas)
        drawDoors(app, canvas)
        drawPlayerAttacks(app, canvas)
        drawMonsters(app, canvas)
        drawBossAttacks(app, canvas)
        drawPlayerHealth(app, canvas)


#####################
#Drawing Functions
#####################
def drawPlayer(app, canvas):
    player = app.player
    canvas.create_rectangle(player.cx - player.width, 
    player.cy - player.width, player.cx + player.width, player.cy + player.width, fill='medium purple')

def drawPlayerAttacks(app, canvas):
    for attack in app.currentRoom.playerAttacks:
        cx = attack['cx']
        cy = attack['cy']
        r = attack['radius']
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='firebrick1')

def drawBossAttacks(app, canvas):
    for attack in app.currentRoom.bossAttacks:
        cx = attack['cx']
        cy = attack['cy']
        r = attack['radius']
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='blue')

def drawRoom(app, canvas):
    if app.currentRoom == app.bossRoom and app.currentRoom.hasPlayer:
        color = 'dark slate gray'
    else:
        color = 'light grey'
    canvas.create_rectangle(0, 0, app.width, app.height, fill=color)

#make doors resizable to the window in the future
def drawDoors(app, canvas):
    dirs = [(0,-1),(0,+1),(-1,0),(+1,0)]
    if len(app.currentRoom.monsters) != 0: color = 'dim gray'
    else: color = 'dark grey'
    for drow, dcol in dirs:
        if checkIfAdjacentRoom(app, (drow,dcol)):
            if drow == -1: #top door
                canvas.create_rectangle(app.doors['top'][0], app.doors['top'][1], app.doors['top'][2], app.doors['top'][3], fill=color)
            elif drow == +1: #bottom door
                canvas.create_rectangle(app.doors['bottom'][0], app.doors['bottom'][1], app.doors['bottom'][2], app.doors['bottom'][3], fill=color)
            elif dcol == -1: #left door
                canvas.create_rectangle(app.doors['left'][0], app.doors['left'][1], app.doors['left'][2], app.doors['left'][3], fill=color)
            elif dcol == +1: #right door
                canvas.create_rectangle(app.doors['right'][0], app.doors['right'][1], app.doors['right'][2], app.doors['right'][3], fill=color)

def drawMonsters(app, canvas):
    for monster in app.currentRoom.monsters:
        canvas.create_rectangle(monster.cx - monster.width,
            monster.cy - monster.width, monster.cx + monster.width, monster.cy + monster.width, fill='green')

def drawPlayerHealth(app, canvas):
    x0,y0,x1,y1 = 40,20,202,40
    canvas.create_rectangle(x0,y0,x1,y1, fill='white', width=2)
    healthBarWidth = 160
    cellWidth = healthBarWidth / (6 * 2) #app.player.health * 2(because monsters hit 0.5)
    for i in range(app.player.health):
        canvas.create_rectangle(i * cellWidth + 41, 21, (i * cellWidth + 41) + cellWidth, 39, fill='red', width=0)

def drawDoorToNextFloor(app, canvas):
    if len(app.bossRoom.monsters) == 0 and app.currentRoom == app.bossRoom:
        doorWidth = 30
        canvas.create_rectangle(app.width//2 - doorWidth, app.height//2 - doorWidth,
            app.width//2 + doorWidth, app.height//2 + doorWidth, fill='black')

def drawGameOver(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill='black')
    canvas.create_text(app.width//2, app.height//2, text='GAMEOVER!\nYOU DIED!\nPress r to restart', fill='yellow', font='Arial 24 bold')



##############
runApp(width=800, height=600)
##############
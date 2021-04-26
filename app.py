from cmu_112_graphics import *
from classes import *
from functions import * 
import random, math, string

def appStarted(app):
    app.rooms = Room.generateRooms(Room)
    for room in app.rooms:
        if room.hasPlayer:
            app.player = room.player = Player(app.width, app.height)
            app.currentRoom = room
    #for some reason I had to make two loops, instead of putting this check in the above loop. It would create two instances of the starting Room, one with 0 monsters, and the other with 1 monster.
    for room in app.rooms:
        if room.cell != (5,5):
            for i in range(random.randint(1,5)):
                room.generateMonster(Monster(app.width,app.height))
    app.doorWidth = 40
    app.doors = {
        'top':[app.width//2 - app.doorWidth, 0, app.width//2 + app.doorWidth, app.doorWidth//3], 
        'bottom':[app.width//2 - app.doorWidth, app.height - app.doorWidth//3, app.width//2 + app.doorWidth, app.height],
        'left':[0, app.height//2 - app.doorWidth, app.doorWidth//3, app.height//2 + app.doorWidth],
        'right':[app.width - app.doorWidth//3, app.height//2 - app.doorWidth, app.width, app.height//2 + app.doorWidth]
    }
    app.gameOver = False
    print(app.currentRoom)
    
def mousePressed(app, event):
    app.currentRoom.playerAttacks.append(app.player.attack(event.x, event.y))

def keyPressed(app, event):
    if event.key == 'r':
        Room.rooms = []
        appStarted(app)
    playerMovement(app, event)

def timerFired(app):
    if len(app.currentRoom.playerAttacks) > 0:
        movePlayerAttacks(app)
    if app.player.health <= 0:
        app.gameOver = True
    monsterAttack(app)

def redrawAll(app, canvas):
    if app.gameOver:
        drawGameOver(app, canvas)
    else:
        for room in app.rooms:
            if room.hasPlayer: 
                drawRoom(app, canvas, room)
                drawPlayer(app, canvas)
                drawPlayerAttacks(app, canvas)
                drawMonsters(app, canvas)

def drawPlayer(app, canvas):
    player = app.player
    canvas.create_rectangle(player.cx - player.width, 
    player.cy - player.width, player.cx + player.width, player.cy + player.width, fill='light blue')

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
    clr = 'dark grey'
    for drow, dcol in dirs:
        if checkIfAdjacentRoom(app, (drow,dcol)):
            if drow == -1: #top door
                canvas.create_rectangle(app.doors['top'][0], app.doors['top'][1], app.doors['top'][2], app.doors['top'][3], fill=clr)
            elif drow == +1: #bottom door
                canvas.create_rectangle(app.doors['bottom'][0], app.doors['bottom'][1], app.doors['bottom'][2], app.doors['bottom'][3], fill=clr)
            elif dcol == -1: #left door
                canvas.create_rectangle(app.doors['left'][0], app.doors['left'][1], app.doors['left'][2], app.doors['left'][3], fill=clr)
            elif dcol == +1: #right door
                canvas.create_rectangle(app.doors['right'][0], app.doors['right'][1], app.doors['right'][2], app.doors['right'][3], fill=clr)

def drawMonsters(app, canvas):
    for monster in app.currentRoom.monsters:
        canvas.create_rectangle(monster.cx - monster.width,
            monster.cy - monster.width, monster.cx + monster.width, monster.cy + monster.width, fill='green')


def drawGameOver(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill='black')
    canvas.create_text(app.width//2, app.height//2, text='GAMEOVER!\nYOU DIED!\nPress r to restart', fill='yellow', font='Arial 24 bold')

runApp(width=800, height=600)
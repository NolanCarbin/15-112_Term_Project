from rooms import *
from monsters import *

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
        radius = 8
        cx, cy = self.cx, self.cy
        deltaX, deltaY = self.findAttackDeltas(x, y, cx, cy)
        app.currentRoom.playerAttacks.append([cx, cy, radius, deltaX, deltaY])

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
        else: 
            return 
        return (deltaX, deltaY)

    def attackWithKeys(self,app, key):
        if key not in ['Right', 'Left', 'Up', 'Down']: return 
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
        app.currentRoom.playerAttacks.append([cx, cy, radius, deltaX, deltaY])

def playerMovement(app, key):
    if key == 'w':
        app.player.cy -= app.player.movementSpeed
    elif key == 's':
        app.player.cy += app.player.movementSpeed
    elif key == 'a':
        app.player.cx -= app.player.movementSpeed
    elif key == 'd':
        app.player.cx += app.player.movementSpeed
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
            if monster.attackInBoundsOfMonster(attack[0], attack[1], attack[2]):
                if attack in app.currentRoom.playerAttacks:
                    app.currentRoom.playerAttacks.remove(attack)                
                    monster.health -= 1
                if monster.health == 0:
                    app.currentRoom.monsters.remove(monster)



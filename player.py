from rooms import *
from monsters import *

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

def playerMovement(app, key):
    if key in ['w', 'Up']:
        app.player.cy -= app.player.movementSpeed
    elif key in ['s', 'Down']:
        app.player.cy += app.player.movementSpeed
    elif key in ['a', 'Left']:
        app.player.cx -= app.player.movementSpeed
    elif key in ['d', 'Right']:
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
            if attackInBoundsOfMonster(attack[0], attack[1], attack[2], 
                                       monster.cx, monster.cy, monster.width): 
                app.currentRoom.playerAttacks.remove(attack)                
                monster.health -= 1
                if monster.health == 0:
                    app.currentRoom.monsters.remove(monster)

def f(x):
    print('yes')


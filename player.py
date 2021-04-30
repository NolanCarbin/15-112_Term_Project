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
        deltaX = (x - cx) / self.attackSpeed
        deltaY = (y - cy) / self.attackSpeed
        app.currentRoom.playerAttacks.append({'cx': cx, 'cy': cy, 'radius': radius, 'deltaX': deltaX, 'deltaY':deltaY})

    def attackWithKeys(self, app, key):
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



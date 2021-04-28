import math

class Monster(object):
    def __init__(self, cx, cy):
        self.width = 20
        self.cx = cx
        self.cy = cy
        self.speed = 10
        self.health = 5

    def __repr__(self):
        return f'Monster(Location:{(self.cx, self.cy)}, Health:{self.health})'

def monsterAttack(app):
    if len(app.currentRoom.monsters) == 0: return 
    for monster in app.currentRoom.monsters:
        if(app.player.cx - app.player.width <= monster.cx + monster.width and 
           app.player.cx + app.player.width >= monster.cx - monster.width and 
           app.player.cy - app.player.width <= monster.cy + monster.width and 
           app.player.cy + app.player.width >= monster.cy - monster.width):    
            app.player.health -= 0.5

#taken from: http://www.jeffreythompson.org/collision-detection/circle-rect.php 
#converted from another language to python 
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
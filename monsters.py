import math
from StacksAndQueues import Queue

class Monster(object):
    def __init__(self, cx, cy):
        self.width = 20
        self.cx = cx
        self.cy = cy
        #movementSpeed is inverted, lower == faster
        self.movementSpeed = 6
        #physical attack speed:
        self.attackSpeed = 6
        self.health = 6

    def __repr__(self):
        return f'Monster(Location:{(self.cx, self.cy)}, Health:{self.health})'

    #################
    #Monster Methods
    #################
    
    #path() and findPlayer() are taken from: 
    # https://www.redblobgames.com/pathfinding/a-star/introduction.html
    #findPlayer() uses BFS to tell if there is a path from the monster to the 
    #player, and path() returns the path from the current cell of the monster 
    #to the cell nearest to the player. I interpreted the code from the site, 
    #and used it to fit my needs. Instead checking if the currentNode == goalNode
    #I made it check if the currentNode(monster's cell) was in the bounds of the the player's cell.

    @staticmethod
    def path(goalCell, cameFrom, startingCell):
        current = goalCell
        endPath = []
        while current != startingCell:
            endPath.append(current)
            current = cameFrom[current]
        endPath.reverse()
        return endPath

    def findPlayer(self, graph, player):
        def inBounds(currentNode, player):
            nodeX, nodeY = currentNode
            if (player.cx - player.width <= nodeX + player.width and 
            player.cx + player.width >= nodeX - player.width and 
            player.cy - player.width <= nodeY + player.width and 
            player.cy + player.width >= nodeY - player.width):
                return True
            return False
        startingCell = (self.cx, self.cy)
        queue = Queue()
        cameFrom = dict()
        queue.enqueue(startingCell) 
        cameFrom[startingCell] = None
        while queue.len() != 0:
            currentNode = queue.dequeue()
            if inBounds(currentNode, player): 
                return Monster.path(currentNode, cameFrom, startingCell)
            for node in graph[currentNode]:
                if node not in cameFrom:
                    cameFrom[node] = currentNode
                    queue.enqueue(node)
        return None

    def moveTowardPlayer(self, app):
        path = self.findPlayer(app.currentRoom.graph, app.player)
        if path != None and len(path) >= 1:
            self.cx = path[0][0]
            self.cy = path[0][1]
    
    def inBoundsOfPlayer(self, app):
        if (app.player.cx - app.player.width <= self.cx + self.width and 
            app.player.cx + app.player.width >= self.cx - self.width and 
            app.player.cy - app.player.width <= self.cy + self.width and 
            app.player.cy + app.player.width >= self.cy - self.width): 
                if app.cheatsOn: return
                app.player.health -= 1

    #taken from: https://www.geeksforgeeks.org/check-if-any-point-overlaps-the-given-circle-and-rectangle/
    #modified to be a method and fit the needs of my app
    def attackInBoundsOfMonster(self, circleX, circleY, r): 
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


class BossMonster(Monster):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.width = 40
        #movementSpeed is inverted, lower == faster
        self.movementSpeed = 8
        #physical attack speed:
        self.attackSpeed = 2
        #inverted lower == faster
        self.shootingSpeed = 10
        self.health = 25

    def attackPlayer(self, app):
        cx = self.cx
        cy = self.cy
        radius = 8
        deltaX = (app.player.cx - cx) / self.shootingSpeed
        deltaY = (app.player.cy - cy) / self.shootingSpeed
        app.currentRoom.bossAttacks.append({'cx': cx, 'cy': cy, 'radius': radius, 'deltaX': deltaX, 'deltaY':deltaY})

    @staticmethod
    def moveBossAttacks(app):
        for attack in app.currentRoom.bossAttacks: 
            attack['cx'] = attack['cx'] + attack['deltaX']
            attack['cy'] = attack['cy'] + attack['deltaY']
            #check if not inBoundsOfRoom:
            if (attack['cx'] < 0 or attack['cx'] > app.width or 
                attack['cy'] < 0 or attack['cy'] > app.height): 
                app.currentRoom.bossAttacks.remove(attack)
            #check if inBoundsOfPlayer:
            if app.player.attackInBoundsOfPlayer(attack['cx'], attack['cy'], attack['radius']):
                if attack in app.currentRoom.bossAttacks:
                    app.currentRoom.bossAttacks.remove(attack)
                    if app.cheatsOn: return                
                    app.player.health -= 1
    
class BatMonster(Monster):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.width = 20
        #movementSpeed is inverted, lower == faster
        self.movementSpeed = 3
        #physical attack speed:
        self.attackSpeed = 12
        self.health = 2
        self.pathToPlayer = []
    
    def __repr__(self):
        return f'BatMonster(Location:{(self.cx, self.cy)}, Health:{self.health})'

    def moveTowardPlayer(self, app):
        if len(self.pathToPlayer) == 0:
            self.pathToPlayer = self.findPlayer(app.currentRoom.graph, app.player)
        if len(self.pathToPlayer) >= 1:
            self.cx = self.pathToPlayer[0][0]
            self.cy = self.pathToPlayer[0][1]
            self.pathToPlayer = self.pathToPlayer[1:]
            

import math
from StacksAndQueues import Queue

class Monster(object):
    def __init__(self, cx, cy):
        self.width = 20
        self.cx = cx
        self.cy = cy
        self.speed = 10
        self.health = 5

    def __repr__(self):
        return f'Monster(Location:{(self.cx, self.cy)}, Health:{self.health})'

    #################
    #Monster Methods
    #################

    @staticmethod
    def path(goalCell, cameFrom, startingCell):
        current = goalCell
        endPath = []
        while current != startingCell:
            endPath.append(current)
            current = cameFrom[current]
        # endPath.append(startingCell)
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

    def attackPlayer(self, app):
        path = self.findPlayer(app.graph, app.player)
        if len(path) >= 1:
            self.cx = path[0][0]
            self.cy = path[0][1]
        
    
    def inBoundsOfMonster(self, app):
        if (app.player.cx - app.player.width <= self.cx + self.width and 
            app.player.cx + app.player.width >= self.cx - self.width and 
            app.player.cy - app.player.width <= self.cy + self.width and 
            app.player.cy + app.player.width >= self.cy - self.width):    
                app.player.health -= 0.5

    #taken from: http://www.jeffreythompson.org/collision-detection/circle-rect.php 
    #converted from another language to python 
    def attackInBoundsOfMonster(self, circleX, circleY, r):
        testX = circleX
        testY = circleY
        if (circleX < self.cx):        
            testX = self.cx
        elif (circleX > self.cx + self.width):
            testX = self.cx + self.width
        if (circleY < self.cy):
            testY = self.cy
        elif (circleY > self.cy + self.width):
            testY = self.cy + self.width
    #get distance from closest edges
        distX = circleX - testX
        distY = circleY - testY
        distance = math.sqrt((distX * distX) + (distY * distY))
    #if the distance is less than the radius, then collision
        if (distance <= r):
            return True
        return False




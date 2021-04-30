import math
from StacksAndQueues import Queue

class Monster(object):
    def __init__(self, cx, cy):
        self.width = 20
        self.cx = cx
        self.cy = cy
        self.movementSpeed = 8
        self.attackSpeed = 4

        self.health = 5

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
        path = self.findPlayer(app.graph, app.player)
        if len(path) >= 1:
            self.cx = path[0][0]
            self.cy = path[0][1]
        
    
    def inBoundsOfPlayer(self, app):
        if (app.player.cx - app.player.width <= self.cx + self.width and 
            app.player.cx + app.player.width >= self.cx - self.width and 
            app.player.cy - app.player.width <= self.cy + self.width and 
            app.player.cy + app.player.width >= self.cy - self.width):    
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
        self.movementSpeed = 12
        self.attackSpeed = 2
        self.health = 20

    def attackPlayer(self, app):
        pass
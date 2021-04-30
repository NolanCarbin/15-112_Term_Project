L = [(5,5), (4,5), (6,5), (3,5), (5,6), (3,4)]

result = {
    (5,5):{(4,5), (6,5), (5,6)},
    (4,5):{(5,5), (3,5)},
    (6,5):{(5,5)},
    (3,5):{(4,5), (3,4)},
    (5,6):{(5,5)},
    (3,4):{(3,5)}
}

#interval for using a the pixel graph is 10
#interval for using cells is 1
def createAdjacencyList(L, interval):
    def isConnected(x0, y0, x1, y1, interval):
        return ((abs(x0 - x1) == 0 and abs(y0 - y1) == interval) or 
                (abs(x0 - x1) == interval and abs(y0 - y1) == 0))
    graph = dict()
    for nodeRow, nodeCol in L:
        graph[(nodeRow, nodeCol)] = set()
        for edgeRow, edgeCol in L:
            if (nodeRow, nodeCol) != (edgeRow, edgeCol):
                if isConnected(nodeRow, nodeCol, edgeRow, edgeCol, interval):
                    graph[(nodeRow, nodeCol)].add((edgeRow, edgeCol))        
    return graph


def createRoomPixelList(canvasWidth, canvasHeight):
    rows = canvasWidth // 40
    cols = canvasHeight // 40
    result = []
    for row in range(rows):
        for col in range(cols):
            result.append(((row * 40), (col * 40)))
    return result


class Queue(object):
    def __init__(self):
        self.queue = []

    def __repr__(self):
        return f'{self.queue}'

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)
        
    def len(self):
        return len(self.queue)

graph = createAdjacencyList(createRoomPixelList(400, 500), 40)
startingCell = (240, 80)
goalCell = (100, 200)

def path(goalCell, cameFrom, startingCell):
    current = goalCell
    endPath = []
    while current != startingCell:
        endPath.append(current)
        current = cameFrom[current]
    # endPath.append(startingCell)
    endPath.reverse()
    return endPath

def findPlayer(cx, cy, graph, player):
    def inBounds(currentNode, player):
        nodeX, nodeY = currentNode
        if (player.cx - player.width <= nodeX + player.width and 
        player.cx + player.width >= nodeX - player.width and 
        player.cy - player.width <= nodeY + player.width and 
        player.cy + player.width >= nodeY - player.width):
            return True
        return False
    startingCell = (cx, cy)
    queue = Queue()
    cameFrom = dict()
    queue.enqueue(startingCell) 
    cameFrom[startingCell] = None
    while queue.len() != 0:
        currentNode = queue.dequeue()
        if inBounds(currentNode, player): 
            return path(currentNode, cameFrom, startingCell)
        for node in graph[currentNode]:
            if node not in cameFrom:
                cameFrom[node] = currentNode
                queue.enqueue(node)
    return None


print(findPlayer(graph, startingCell, goalCell))
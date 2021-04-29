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
    graph = dict()
    for nodeRow, nodeCol in L:
        graph[(nodeRow, nodeCol)] = set()
        for edgeRow, edgeCol in L:
            if (nodeRow, nodeCol) != (edgeRow, edgeCol):
                if isConnected(nodeRow, nodeCol, edgeRow, edgeCol, interval):
                    graph[(nodeRow, nodeCol)].add((edgeRow, edgeCol))        
    return graph

def isConnected(x0, y0, x1, y1, interval):
    return ((abs(x0 - x1) == 0 and abs(y0 - y1) == interval) or 
    (abs(x0 - x1) == interval and abs(y0 - y1) == 0))

# print(createAdjacencyList(L))


#Use BFS to find the farthest cell from starting cell

#root will equal starting room/cell(5,5)
#create a queue
#what is the goal?
#   calculate the farthest room cell
#   the cell with the most amount of nodes inbetween
def findFarthestRoom(graph, root):
    pass


L = [(10, 10), (10, 20), (10, 30)]

def createRoomPixelList(canvasWidth, canvasHeight):
    rows = canvasHeight // 10
    cols = canvasWidth // 10
    result = []
    for row in range(rows + 1):
        for col in range(cols + 1):
            result.append((row * 10, col * 10))
    return result

print(createRoomPixelList(50,50))


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



graph = createAdjacencyList(createRoomPixelList(100, 100), 10)
startingCell = (10, 50)
goalCell = (20, 20)


def bfs1(graph, startingCell, goalCell):
    queue = Queue()
    visited = set()
    queue.enqueue(startingCell) 
    visited.add(startingCell)
    while queue.len() != 0:
        currentNode = queue.dequeue()
        for node in graph[currentNode]:
            if node not in visited:
                visited.add(node)
                if node == goalCell: return node
                queue.enqueue(node)
    return None

def bfs2(graph, startingCell, goalCell):
    queue = Queue()
    cameFrom = dict()
    queue.enqueue(startingCell) 
    cameFrom[startingCell] = None
    while queue.len() != 0:
        currentNode = queue.dequeue()
        if currentNode == goalCell: return path(goalCell, cameFrom, startingCell)
        for node in graph[currentNode]:
            if node not in cameFrom:
                cameFrom[node] = currentNode
                queue.enqueue(node)
    return None

def path(goal, cameFrom, start):
    current = goal
    endPath = []
    while current != start:
        endPath.append(current)
        current = cameFrom[current]
    endPath.append(start)
    endPath.reverse()
    return endPath

print(bfs2(graph, startingCell, goalCell))
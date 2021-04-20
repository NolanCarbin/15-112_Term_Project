L = [(5,5), (4,5), (6,5), (3,5), (5,6), (3,4)]

result = {
    (5,5):{(4,5), (6,5), (5,6)},
    (4,5):{(5,5), (3,5)},
    (6,5):{(5,5)},
    (3,5):{(4,5), (3,4)},
    (5,6):{(5,5)},
    (3,4):{(3,5)}
}

def createAdjacencyList(L):
    graph = dict()
    for nodeRow, nodeCol in L:
        graph[(nodeRow, nodeCol)] = set()
        for edgeRow, edgeCol in L:
            if (nodeRow, nodeCol) != (edgeRow, edgeCol):
                if isConnected(nodeRow, nodeCol, edgeRow, edgeCol):
                    graph[(nodeRow, nodeCol)].add((edgeRow, edgeCol))        
    return graph

def isConnected(x0, y0, x1, y1):
    return ((abs(x0 - x1) == 0 and abs(y0 - y1) == 1) or 
    (abs(x0 - x1) == 1 and abs(y0 - y1) == 0))

print(createAdjacencyList(L))


#Use BFS to find the farthest cell from starting cell

#root will equal starting room/cell(5,5)
#create a queue
#what is the goal?
#   calculate the farthest room cell
#   the cell with the most amount of nodes inbetween
def findFarthestRoom(graph, root):
    pass
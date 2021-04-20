from cmu_112_graphics import *
import math, random, string

def appStarted(app):
    app.margin = 100
    app.rows = 11
    app.cols = 11
    app.numOfRooms = 10
    app.rooms = []
    app.selectionRooms = []

#influenced by https://youtu.be/tUskxXXTh7s?t=59
def generateRooms(app):
    app.rooms = []
    app.selectionRooms = []
    startingRoom = (app.rows//2, app.cols//2)
    app.rooms.append(startingRoom)
    for i in range(app.numOfRooms):
        roomRow, roomCol = app.rooms[i]
        for drow, dcol in [(-1, 0), (0, +1), (+1, 0), (0, -1)]:
            newRow, newCol = roomRow + drow, roomCol + dcol
            if ((newRow, newCol) not in app.selectionRooms and 
                (newRow, newCol) not in app.rooms and
                 newRow < app.rows and newCol < app.cols):
                app.selectionRooms.append((newRow, newCol))
        randomRoom = random.choice(app.selectionRooms)
        app.rooms.append(randomRoom)
        app.selectionRooms.remove(randomRoom)
    
    
def keyPressed(app, event):
    if event.key == 'r':
        generateRooms(app)

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    drawRooms(app, canvas)

def drawRooms(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            if (row, col) in app.rooms:
                if (row, col) == app.rooms[0]:
                    color = 'light blue'
                elif (row, col) == app.rooms[-1]:
                    color = 'brown'
                else:
                    color = 'green'
                x0, y0, x1, y1 = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill=color)      

def drawGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1)

def getCellBounds(app, row, col):
    gridWidth = app.width - app.margin * 2
    gridHeight = app.height - app. margin * 2
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    y0 = app.margin + row * cellHeight
    x1 = x0 + cellWidth
    y1 = y0 + cellHeight
    return (x0, y0, x1, y1)

runApp(width=1000, height=640)
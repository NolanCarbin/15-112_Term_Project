from cmu_112_graphics import *
import time

def appStarted(app):
    app.cx = 20
    app.cy = app.height//2
    app.keyPressedTimer = None
    app.totalKeyPressedTimer = None
    app.lastKeyPressed = None

def keyPressed(app, event):
    app.keyPressedTimer = time.time()
    app.totalKeyPressedTimer = time.time()
    app.lastKeyPressed = event.key
    playerMovement(app, event)

def keyReleased(app, event):
    app.keyPressedTimer = None
    app.totalKeyPressedTimer = None
    app.lastKeyPressed = None

def timerFired(app):
    if app.keyPressedTimer != None and time.time() - app.keyPressedTimer >= 0.02:
        timerFunction(app, app.lastKeyPressed) 
        app.keyPressedTimer = time.time() #reset the timer

    #Lets the OS repeat the function call
    if app.totalKeyPressedTimer != None and time.time() - app.totalKeyPressedTimer >= 0.5: 
        app.keyPressedTimer = None
        app.totalKeyPressedTimer = None

def timerFunction(app, key):
    if key == 'd':
        app.cx += 5
    elif key == 'a':
        app.cx -= 5

def playerMovement(app, event):
    if event.key == 'd':
        app.cx += 5
    elif event.key == 'a':
        app.cx -= 5
    elif event.key == 'r':
        app.cx = 20

def redrawAll(app, canvas):
    canvas.create_oval(app.cx - 10, app.cy - 10, app.cx + 10, app.cy + 10, fill='red')

runApp(width=900, height=400)
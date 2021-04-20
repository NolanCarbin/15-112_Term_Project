#influenced from the spritesheet section of https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

#sprite image taken from: https://luizmelo.itch.io/wizard-pack

from cmu_112_graphics import *

def appStarted(app):
    idleImage = 'images/Wizard Pack/Idle.png'
    attack1Image = 'images/Wizard Pack/Attack1.png'
    attack2Image = 'images/Wizard Pack/Attack2.png'
    runImage = 'images/Wizard Pack/Run.png'
    attack1Spritestrip = app.loadImage(attack1Image)
    attack2Spritestrip = app.loadImage(attack2Image)
    idleSpritestrip = app.loadImage(idleImage)
    runSpritestrip = app.loadImage(runImage)
    app.idleSprites = []
    app.runSprites = []
    app.attack1Sprites = []
    app.attack2Sprites = []
    app.cx, app.cy = app.width//2, app.height//2
    app.movementSpeed = 10
    app.idleSpriteCounter = app.attackingCounter = app.runningCounter = 0
    app.flipped = app.isMoving = app.attacking1 = app.attacking2 = False
    #idle spritestrip
    for i in range(6):
        sprite = idleSpritestrip.crop((68 + i * 231, 15, 150 + i * 231, 140))
        app.idleSprites.append(sprite)
    #attack1 spritestrip
    for i in range(8):
        sprite = attack1Spritestrip.crop((68 + i * 231, 15, 230 + i * 231, 140))
        app.attack1Sprites.append(sprite)
    #attack2 spritestrip
    for i in range(8):
        sprite = attack2Spritestrip.crop((68 + i * 231, 15, 230 + i * 231, 140))
        app.attack2Sprites.append(sprite)
    #run spritestrip
    for i in range(8):
        sprite = runSpritestrip.crop((68 + i * 231, 15, 150 + i * 231, 140))
        app.runSprites.append(sprite)


def keyPressed(app, event):
    if event.key in ['w', 'Up']: app.cy -= app.movementSpeed
    elif event.key in ['s', 'Down']: app.cy += app.movementSpeed
    elif event.key in ['a', 'Left']: 
        app.cx -= app.movementSpeed
        app.isMoving = True
        if not app.flipped:
            app.flipped = True
            for i in range(len(app.idleSprites)):
                app.idleSprites[i] = app.idleSprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            for i in range(len(app.attack1Sprites)):
                app.attack1Sprites[i] = app.attack1Sprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            for i in range(len(app.attack2Sprites)):
                app.attack2Sprites[i] = app.attack2Sprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            for i in range(len(app.runSprites)):
                app.runSprites[i] = app.runSprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            

    elif event.key in ['d', 'Right']: 
        app.cx += app.movementSpeed
        app.isMoving = True
        if app.flipped:
            app.flipped = False
            for i in range(len(app.idleSprites)):
                app.idleSprites[i] = app.idleSprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            for i in range(len(app.attack1Sprites)):
                app.attack1Sprites[i] = app.attack1Sprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            for i in range(len(app.attack2Sprites)):
                app.attack2Sprites[i] = app.attack2Sprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            for i in range(len(app.runSprites)):
                app.runSprites[i] = app.runSprites[i].transpose(Image.FLIP_LEFT_RIGHT)
            
    elif event.key == 'Space': 
        app.attackingCounter = 0
        app.attacking1 = True

def mousePressed(app, event):
    app.attackingCounter = 0
    app.attacking2 = True

def keyReleased(app, event):
    if event.key in ['w','a','s','d','Up','Left','Right','Down']:
        app.isMoving = False

def timerFired(app):
    if app.attacking1 or app.attacking2:
        app.attackingCounter = (1 + app.attackingCounter) % len(app.attack1Sprites)
        if app.attackingCounter == len(app.attack1Sprites) - 1:
            app.attacking1 = app.attacking2 = False
    elif app.isMoving:
        app.runningCounter = (1 + app.runningCounter) % len(app.runSprites)
    else: 
        app.idleSpriteCounter = (1 + app.idleSpriteCounter) % len(app.idleSprites)

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='light grey')
    if app.attacking1:
        sprite = app.attack1Sprites[app.attackingCounter]
        canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(sprite))
    elif app.attacking2:
        sprite = app.attack2Sprites[app.attackingCounter]
        canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(sprite))
    elif app.isMoving:
        sprite = app.runSprites[app.runningCounter]
        canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(sprite))
    else:
        sprite = app.idleSprites[app.idleSpriteCounter]
        canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(sprite))
    # canvas.create_rectangle(app.cx - 16, app.cy - 14, app.cx + 16, app.cy + 62) #hitbox

def appStopped(app):
    pass

runApp(width=600, height=500)










# def appStarted(app):
#     backgroundSource = 'images/dungeonBackground.png'
#     imageSource = 'images/Wizard Pack/Idle.png'
#     app.image = app.loadImage(imageSource)
#     app.backgroundImage = app.loadImage(backgroundSource)
#     app.scaledBackgroundImage = app.scaleImage(app.backgroundImage, .8)
#     app.croppedImage = app.image.crop((80, 50, 150, 150))
#     app.scaledImage = app.scaleImage(app.croppedImage, .7)
#     app.cx = app.width // 2
#     app.cy = app.height // 2
#     app.flipped = False

# def keyPressed(app, event):
#     if event.key in ['w', 'Up']: app.cy -= 5
#     elif event.key in ['s', 'Down']: app.cy += 5
#     elif event.key in ['a', 'Left']: 
#         app.cx -= 5
#         if not app.flipped:
#             app.scaledImage = app.scaledImage.transpose(Image.FLIP_LEFT_RIGHT)
#             app.flipped = True
#     elif event.key in ['d', 'Right']: 
#         app.cx += 5
#         if app.flipped:
#             app.scaledImage = app.scaledImage.transpose(Image.FLIP_LEFT_RIGHT)
#             app.flipped = False

# def redrawAll(app, canvas):
#     canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.scaledBackgroundImage))
#     canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.scaledImage))
# runApp(width=750, height=575)


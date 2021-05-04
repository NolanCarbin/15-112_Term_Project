from cmu_112_graphics import *
from monsters import *
from player import * 
from rooms import *
from sprites import *
import random, time

#############
#Main App
#############

def appStarted(app):
    app.floorNumber = 0
    app.doorWidth = 40
    app.nextDoorWidth = 20
    app.itemsWidth = 10
    app.itemFunctions = {'healthPack': healthPack, 'speedUp': speedUp, 'damageUp': damageUp, 'increaseManaRegen': increaseManaRegen, 'hpUp':hpUp}
    app.doors = {
        'top':[app.width//2 - app.doorWidth, 0, 
               app.width//2 + app.doorWidth, app.doorWidth//3], 
        'bottom':[app.width//2 - app.doorWidth, app.height - app.doorWidth//3, 
                  app.width//2 + app.doorWidth, app.height],
        'left':[0, app.height//2 - app.doorWidth, 
                app.doorWidth//3, app.height//2 + app.doorWidth],
        'right':[app.width - app.doorWidth//3, app.height//2 - app.doorWidth, 
                 app.width, app.height//2 + app.doorWidth]
    }
    initializeWorld(app)
    initializePlayerAndMonsters(app)
    initializeSprites(app)
    app.gameOver = False
    app.cheatsOn = False
    ##################
    app.keyPressedTimer = None
    app.totalKeyPressedTimer = None
    app.lastKeyPressed = None
    ##################
    app.monsterMovementTimer = 0
    app.monsterAttackTimer = 0
    app.bossAttackTimer = 0
    ##################
    print(app.currentRoom)

def initializeWorld(app):
    app.rooms = Room.generateRooms(Room)
    for room in app.rooms:
        #Adds rocks to the room
        if room.cell != (0,0):
            roomPixelList = Room.createRoomPixelList(app.width, app.height) 
            #select a couple of random cells in the pixel list
            for i in range(random.randint(8,15)):
                randomCell = findRockRandomCell(app, roomPixelList)
                # add them to the room.rocks list
                room.rocks.append(randomCell)
                #remove them from the list 
                roomPixelList.remove(randomCell)
            #add items:
            chance = random.randrange(1,10)
            #30% chance to add a random item(x,y,function)
            if chance in {1,2,3}:
                randomItem = random.choice(list(app.itemFunctions.keys()))
                itemData = {'cell': random.choice(roomPixelList), 'function':app.itemFunctions[randomItem], 'name': randomItem}
                room.items.append(itemData)
            ####################
            #creates the graph for the specific room
            room.graph = Room.createAdjacencyList(roomPixelList, 40)
            ####################
    #Adds 3 health packs in 3 random rooms
    for i in range(3):
        randomRoom = random.choice(app.rooms)
        itemData = {'cell': random.choice(roomPixelList), 'function':app.itemFunctions['healthPack'], 'name': 'healthPack'}
        randomRoom.items.append(itemData)
    #Creates a graph of the rooms not the pixels/used to find the farthest room/boss room
    app.roomGraph = Room.createAdjacencyList(Room.createRoomList(), 1)

def initializePlayerAndMonsters(app):
    #sets up player:
    for room in app.rooms:
        if room.hasPlayer:
            app.player = room.player = Player(app.width, app.height)
            app.currentRoom = room
    farthestRoomCell = Room.findFarthestRoom(app.roomGraph, app.currentRoom.cell)
    #sets up monsters and boss:
    for room in app.rooms:
        if room.cell == farthestRoomCell:
            app.bossRoom = room
            room.isBossRoom = True
            room.generateBoss(room.graph, app.width, app.height)
        if room.cell != (0,0) and room.cell != farthestRoomCell:
            for i in range(random.randint(2,5)):
                room.generateMonster(room.graph, app.width, app.height)
    
def initializeSprites(app):
    #Sprites:
    app.wizard = PlayerSpritesheet(app, 'images/wizardSpritesheet.png')
    app.wizard.scaleImage(app, .7)
    app.wizard.initializeIdleSpriteList()
    app.wizard.initializeRunningSpriteList()
    app.wizard.initializeAttackSpriteList()
    app.skeleton = MonsterSpritesheet(app, 'images/skeletonSpritesheet.png')
    app.skeleton.scaleImage(app, 1.7)
    app.skeleton.initializeRunningSpriteList(1.7)
    app.bat = BatSpritesheet(app, 'images/batSpritesheet.png')
    app.bat.scaleImage(app, 3)
    app.bat.initializeRunningSpriteList(3)
    app.boss = BossSpritesheet(app, 'images/cyclopsspritesheet.png')
    app.boss.scaleImage(app, 3)
    app.boss.initializeRunningSpriteList(3)
    app.rocksImage = Spritesheet(app, 'images/stones.png')
    app.rocksImage.cropImage(6,539,112,630)
    app.rocksImage.scaleImage(app, .5)



def findRockRandomCell(app, roomList):
    middleX = app.width//2
    middleY = app.height//2
    dWidth = app.doorWidth
    #These are cells/nodes that are right around each of the 4 doors. 
    #This makes sure that no rock spawns right in front of the door causing the player
    #to be stuck and not able to proceed to the next room.
    topDoorSet = {(middleX,0),(middleX,dWidth),(middleX,dWidth*2),(middleX - dWidth,0),
                  (middleX-dWidth,dWidth),(middleX+dWidth,0),(middleX+dWidth,dWidth)}
    bottomDoorSet = {(middleX,app.height-dWidth),(middleX,app.height-(dWidth*2)),
                     (middleX-dWidth,app.height-dWidth),(middleX-dWidth,app.height-(dWidth*2)),
                     (middleX+dWidth,app.height-dWidth),(middleX+dWidth,app.height-(dWidth*2))}
    leftDoorSet = {(0,middleY),(dWidth,middleY),(0,middleY-dWidth),(dWidth,middleY-dWidth),
                   (0,middleY+dWidth),(dWidth,middleY+dWidth)}
    rightDoorSet = {(app.width-dWidth,middleY),(app.width-(dWidth*2),middleY),
                    (app.width-dWidth,middleY-dWidth),(app.width-(dWidth*2),middleY-dWidth),
                    (app.width-dWidth,middleY+dWidth),(app.width-(dWidth*2),middleY+dWidth)}
    randomCell = random.choice(roomList)
    while (randomCell in topDoorSet or randomCell in bottomDoorSet or 
           randomCell in leftDoorSet or randomCell in rightDoorSet):
        randomCell = random.choice(roomList)
    return randomCell

def mousePressed(app, event):
    app.player.attackWithMouse(app, event.x, event.y)
  
def keyPressed(app, event):
    #Used for the os delay:
    ###################
    app.keyPressedTimer = time.time()
    app.totalKeyPressedTimer = time.time()
    app.lastKeyPressed = event.key
    ###################
    if event.key == 'r':
        restartApp(app)
    playerMovement(app, event.key)
    app.player.attackWithKeys(app, event.key)
    if event.key == 'b':
        app.currentRoom.hasPlayer = False
        app.currentRoom.player = None
        app.currentRoom = app.bossRoom 
        app.currentRoom.hasPlayer = True
        app.currentRoom.player = app.player
    if event.key == 'c':
        app.cheatsOn = not app.cheatsOn
        if app.cheatsOn: print('Cheats are now on')
        else: print('Cheats are now off')
def restartApp(app):
    Room.rooms = []
    Room.selectionRooms = []
    appStarted(app)

def advanceToNextFloor(app):
    currentFloorNumber = app.floorNumber
    Room.rooms = []
    Room.selectionRooms = []
    #Old Player Stats:
    playersCurrentHealth = app.player.health
    movementSpeed = app.player.movementSpeed
    totalHealth = app.player.totalHealth
    attackDamage = app.player.attackDamage
    totalMana = app.player.totalMana
    manaRegenSpeed = app.player.manaRegenSpeed
    #Reset:
    appStarted(app)
    #Previous Player Stats:
    app.floorNumber = currentFloorNumber + 1
    app.player.health = playersCurrentHealth
    app.player.movementSpeed = movementSpeed
    app.player.totalHealth = totalHealth
    app.player.attackDamage = attackDamage 
    app.player.totalMana = totalMana
    app.player.manaRegenSpeed = manaRegenSpeed

def keyReleased(app, event):
    app.keyPressedTimer = None
    app.totalKeyPressedTimer = None
    app.lastKeyPressed = None
    app.wizard.isRunning = False

def timerFired(app):
    #Used for the os delay:
    ##################
    if app.keyPressedTimer != None and time.time() - app.keyPressedTimer >= 0.02:
        playerMovement(app, app.lastKeyPressed) 
        app.keyPressedTimer = time.time() #reset the timer
    #Lets the OS repeat the function call
    if app.totalKeyPressedTimer != None and time.time() - app.totalKeyPressedTimer >= 0.5: 
        app.keyPressedTimer = None
        app.totalKeyPressedTimer = None
    # ##################
    #Player and bosses shooting attacks
    if len(app.currentRoom.playerAttacks) > 0:
        movePlayerAttacks(app)
    if len(app.currentRoom.bossAttacks) > 0:
        BossMonster.moveBossAttacks(app)
    ###################
    #Player mana:
    if app.player.mana < app.player.totalMana:
        app.player.manaTimer += 1
        if app.player.manaTimer % app.player.manaRegenSpeed == 0: 
            app.player.mana += 1
    ####################
    if app.player.health <= 0:
        app.gameOver = True
    ###################
    #Monster/Boss movement and attack speeds
    app.monsterMovementTimer += 1
    app.monsterAttackTimer += 1
    app.bossAttackTimer += 1
    for monster in app.currentRoom.monsters:
        if len(app.currentRoom.monsters) == 0: return 
        if app.monsterMovementTimer % monster.movementSpeed == 0:
            monster.moveTowardPlayer(app)
        #The lower the attackSpeed the faster the monsters hit
        if app.monsterMovementTimer % (monster.attackSpeed - app.floorNumber) == 0:
            monster.inBoundsOfPlayer(app)
        if app.currentRoom == app.bossRoom:
            if app.bossAttackTimer % monster.shootingSpeed == 0:
                monster.attackPlayer(app)
    ###################
    #Checks if player killed the boss and if is in bounds of the floor door
    if (len(app.bossRoom.monsters) == 0 and app.currentRoom.hasPlayer and 
           (app.player.cx - app.player.width <= app.width//2 + app.nextDoorWidth and 
            app.player.cx + app.player.width >= app.width//2 - app.nextDoorWidth and 
            app.player.cy - app.player.width <= app.height//2 + app.nextDoorWidth and 
            app.player.cy + app.player.width >= app.height//2 - app.nextDoorWidth)):
        advanceToNextFloor(app)
    ###################
    #Sprites:
    if app.wizard.attacking:
        app.wizard.incrementAttackingCounter()
    elif app.wizard.isRunning:
        app.wizard.incrementRunningCounter()
    else:
        app.wizard.incrementIdleCounter()
    app.skeleton.incrementRunningCounter()
    app.boss.incrementRunningCounter()
    app.bat.incrementRunningCounter()

    #Flips monster's sprites:
    if app.player.cx < app.width//2 and not app.skeleton.flipped: 
        app.skeleton.flipSpriteSheet(app.skeleton.runningSprites)
        app.skeleton.flipped = True
        app.boss.flipSpriteSheet(app.boss.runningSprites)
        app.boss.flipped =True
    elif app.player.cx >= app.width//2 and app.skeleton.flipped:
        app.skeleton.flipSpriteSheet(app.skeleton.runningSprites)
        app.skeleton.flipped = False
        app.boss.flipSpriteSheet(app.boss.runningSprites)
        app.boss.flipped = False
    ###################

def redrawAll(app, canvas):
    if app.gameOver:
        drawGameOver(app, canvas)
    else:
        drawRoom(app, canvas)
        drawRocks(app, canvas)
        drawDoorToNextFloor(app, canvas)
        drawPlayer(app, canvas)
        drawDoors(app, canvas)
        drawPlayerAttacks(app, canvas)
        drawMonsters(app, canvas)
        drawBossAttacks(app, canvas)
        drawPlayerHealthAndMana(app, canvas)
        drawMonstersHealth(app, canvas)
        drawItems(app, canvas)



#####################
#Drawing Functions
#####################

def drawPlayer(app, canvas):
    #HitBox:
    # canvas.create_rectangle(app.player.cx - app.player.width, 
    #     app.player.cy - app.player.width, app.player.cx + app.player.width, 
    #     app.player.cy + app.player.width, fill='medium purple')
    #Sprite:
    if app.wizard.attacking:
        sprite = app.wizard.attackSprites[app.wizard.attackingCounter]
    elif app.wizard.isRunning:
        sprite = app.wizard.runningSprites[app.wizard.runningCounter]
    else:
        sprite = app.wizard.idleSprites[app.wizard.idleSpriteCounter]
    canvas.create_image(app.player.cx, app.player.cy, image=ImageTk.PhotoImage(sprite))

def drawPlayerAttacks(app, canvas):
    for attack in app.currentRoom.playerAttacks:
        cx = attack['cx']
        cy = attack['cy']
        r = attack['radius']
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='white')

def drawBossAttacks(app, canvas):
    color = 'firebrick2'
    for attack in app.currentRoom.bossAttacks:
        cx = attack['cx']
        cy = attack['cy']
        r = attack['radius']
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=color)

def drawRoom(app, canvas):
    if app.currentRoom == app.bossRoom and app.currentRoom.hasPlayer:
        color = 'dark slate gray'
    else:
        color = 'lightblue4'
    canvas.create_rectangle(0, 0, app.width, app.height, fill=color)

#make doors resizable to the window in the future
def drawDoors(app, canvas):
    dirs = [(0,-1),(0,+1),(-1,0),(+1,0)]
    if len(app.currentRoom.monsters) != 0: color = 'dim gray'
    else: color = 'dark grey'
    for drow, dcol in dirs:
        if checkIfAdjacentRoom(app, (drow,dcol)):
            if drow == -1: #top door
                canvas.create_rectangle(app.doors['top'][0], app.doors['top'][1], app.doors['top'][2], app.doors['top'][3], fill=color)
            elif drow == +1: #bottom door
                canvas.create_rectangle(app.doors['bottom'][0], app.doors['bottom'][1], app.doors['bottom'][2], app.doors['bottom'][3], fill=color)
            elif dcol == -1: #left door
                canvas.create_rectangle(app.doors['left'][0], app.doors['left'][1], app.doors['left'][2], app.doors['left'][3], fill=color)
            elif dcol == +1: #right door
                canvas.create_rectangle(app.doors['right'][0], app.doors['right'][1], app.doors['right'][2], app.doors['right'][3], fill=color)

def drawMonsters(app, canvas):
    for monster in app.currentRoom.monsters:
        if app.currentRoom.isBossRoom:
            #Hitbox
            # canvas.create_rectangle(monster.cx - monster.width, 
            #         monster.cy - monster.width, monster.cx + monster.width,
            #         monster.cy + monster.width, fill='green')
            #Sprite
            sprite = app.boss.runningSprites[app.boss.runningCounter]
            canvas.create_image(monster.cx, monster.cy, image=ImageTk.PhotoImage(sprite))
        elif isinstance(monster, BatMonster):
            #Hitbox:
            # canvas.create_rectangle(monster.cx - monster.width, monster.cy - monster.width, 
            #     monster.cx + monster.width, monster.cy + monster.width, fill='red')
            #Sprite:
            sprite = app.bat.runningSprites[app.bat.runningCounter]
            canvas.create_image(monster.cx, monster.cy, image=ImageTk.PhotoImage(sprite))
        else:
        #Hitbox:
            # canvas.create_rectangle(monster.cx - monster.width,
            # monster.cy - monster.width, monster.cx + monster.width, monster.cy + monster.width, fill='green')
        #Sprite:
            sprite = app.skeleton.runningSprites[app.skeleton.runningCounter]
            canvas.create_image(monster.cx, monster.cy, image=ImageTk.PhotoImage(sprite))
    
def drawPlayerHealthAndMana(app, canvas):
    x0,y0,x1,y1 = 40,20,202,40
    canvas.create_rectangle(x0,y0,x1,y1, fill='white', width=2)
    healthBarWidth = 160
    cellWidth = healthBarWidth / (app.player.totalHealth)
    for i in range(app.player.health):
        canvas.create_rectangle(i * cellWidth + 41, 21, (i * cellWidth + 41) + cellWidth, 39, fill='red', width=0)

    x0,y0,x1,y1 = 40,50,161,65
    canvas.create_rectangle(x0,y0,x1,y1, fill='white', width=2)
    manaBarWidth = 120
    cellWidth = manaBarWidth / (app.player.totalMana) #app.player.health * 2(because monsters hit 0.5)
    for i in range(app.player.mana):
        canvas.create_rectangle(i * cellWidth + x0, y0 + 1, (i * cellWidth + x0) + cellWidth, y1 - 1, fill='blue', width=0)

def drawMonstersHealth(app, canvas):
    for monster in app.currentRoom.monsters:
        if isinstance(monster, BossMonster):
            monsterHealth = 25
        elif isinstance(monster, BatMonster):
            monsterHealth = 2
        else:
            monsterHealth = 6
        x0 = monster.cx - monster.width - 3
        y0 = monster.cy - monster.width - 18
        x1 = monster.cx + monster.width + 3
        y1 = monster.cy - monster.width - 15
        canvas.create_rectangle(x0, y0, x1, y1, fill='white')
        healthBarWidth = (monster.cx + monster.width + 3) - (monster.cx - monster.width - 3)
        cellWidth = healthBarWidth / monsterHealth
        for i in range(monster.health):
            canvas.create_rectangle(i * cellWidth + x0, y0, (i * cellWidth + x0) + cellWidth, y1, fill='red', width=0)

def drawDoorToNextFloor(app, canvas):
    if len(app.bossRoom.monsters) == 0 and app.currentRoom == app.bossRoom:
        canvas.create_rectangle(app.width//2 - app.nextDoorWidth, app.height//2 - app.nextDoorWidth,
            app.width//2 + app.nextDoorWidth, app.height//2 + app.nextDoorWidth, fill='black')

def drawRocks(app, canvas):
    for x,y in app.currentRoom.rocks:
        width = app.currentRoom.rockWidth
        # canvas.create_rectangle(x - width, y - width, 
        #                         x + width, y + width, fill='brown')
        canvas.create_image(x,y, image=ImageTk.PhotoImage(app.rocksImage.spritesheet))

def drawItems(app, canvas):
    for dictionary in app.currentRoom.items:
        x,y = dictionary['cell']
        name = dictionary['name']
        if name == 'healthPack':
            color = 'red'
        if name == 'speedUp':
            color = 'yellow'
        if name == 'damageUp':
            color = 'purple' 
        if name == 'increaseManaRegen':
            color = 'blue'
        if name == 'hpUp':
            color = 'brown'
        canvas.create_rectangle(x - app.itemsWidth, y - app.itemsWidth, 
                            x + app.itemsWidth, y + app.itemsWidth, fill=color)

def drawGameOver(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill='black')
    canvas.create_text(app.width//2, app.height//2, text='GAMEOVER!\nYOU DIED!\nPress r to restart', fill='yellow', font='Arial 24 bold')



##############
runApp(width=800, height=640)
##############
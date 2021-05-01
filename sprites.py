from PIL import Image, ImageTk, ImageDraw, ImageFont

class Spritesheet(object):
    def __init__(self, app, filename):
        self.filename = filename
        self.spritesheet = app.loadImage(filename)
        self.idleSprites = []
        self.runningSprites = []
        self.attackSprites = []
        self.idleSpriteCounter = self.attackingCounter = self.runningCounter = 0
        self.flipped = self.isRunning = self.attacking = False
        
    def flipSpriteSheet(self, spritesheet):
        for i in range(len(spritesheet)):
            spritesheet[i] = spritesheet[i].transpose(Image.FLIP_LEFT_RIGHT)
    
    def scaleImage(self, app, scale):
        self.spritesheet = app.scaleImage(self.spritesheet, scale)

    def initializeIdleSpriteList(self):
        for i in range(6):
            sprite = self.spritesheet.crop((48 + i * 162, 40, 104 + i * 162, 100))
            self.idleSprites.append(sprite)

    def initializeRunningSpriteList(self):
        for i in range(14,22):
            sprite = self.spritesheet.crop((48 + i * 162, 40, 104 + i * 162, 100))
            self.runningSprites.append(sprite)

    def initializeAttackSpriteList(self):
        for i in range(6,11):
            sprite = self.spritesheet.crop((48 + i * 162, 40, 126 + i * 162, 100))
            self.attackSprites.append(sprite)
        
    def incrementIdleCounter(self):
        self.idleSpriteCounter = (1 + self.idleSpriteCounter) % len(self.idleSprites)

    def incrementRunningCounter(self):
        self.runningCounter = (1 + self.runningCounter) % len(self.runningSprites)

    def incrementAttackingCounter(self):
        self.attackingCounter = (1 + self.attackingCounter) % len(self.attackSprites)
        if self.attackingCounter == len(self.attackSprites) - 1:
            self.attacking = False

    
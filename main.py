from cmu_graphics import *
from player import *
from pivot import *
from button import *
from wall import *
from spikes import *
from PIL import Image as im
import os, pathlib
import time
import random


def onAppStart(app):
    startGame(app)

def startGame(app):
    # canvas
    app.width = 1000
    app.height = 780
    app.stepsPerSecond = 60
    
    # visuals 
    app.backdrop = openImage("images/background.jpg")
    app.backdropWidth = app.backdrop.width
    app.backdropHeight = app.backdrop.height
    app.backdrop = CMUImage(app.backdrop)

    app.startMenuBackground = openImage("images/menuBackground.jpg")
    app.startMenuBackground = CMUImage(app.startMenuBackground)

    # logo
    app.logo = openImage("images/title.png")
    app.logo = CMUImage(app.logo)

    # start button
    # word images from https://www.fontspace.com/valorax-font-f89146 
    app.startClickedImg = openImage("images/start_clicked.png")
    app.startUnclickedImg = openImage("images/start_unclicked.png")
    app.startButtonInteracted = False
    app.startButton = Button(app.width*0.135, app.height*0.3, 
                             app.startClickedImg.width, 
                             app.startClickedImg.height, 'rectangle')

    # scores button
    # word images from https://www.fontspace.com/valorax-font-f89146
    app.scoresClickedImg = openImage("images/scores_clicked.png")
    app.scoresUnclickedImg = openImage("images/scores_unclicked.png")
    app.scoresButtonInteracted = False
    app.scoresButton = Button(app.width*0.135, app.height*0.4, 
                              app.scoresClickedImg.width, 
                              app.scoresClickedImg.height, 'rectangle')
    
    # help button 
    # word images from https://www.fontspace.com/valorax-font-f89146
    app.helpClickedImg = openImage("images/help_clicked.png")
    app.helpUnclickedImg = openImage("images/help_unclicked.png")
    app.helpButtonInteracted = False
    app.helpButton = Button(app.width*0.135, app.height*0.5, 
                            app.helpClickedImg.width, 
                            app.helpClickedImg.height, 'rectangle')
    
    # instructions screen
    app.instructionsMessage = CMUImage(openImage("images/instructions.png"))

    # Death Notification
    # word images from https://www.fontspace.com/valorax-font-f89146
    app.deathMessage = CMUImage(openImage("images/died.png"))

    # Restart Button from https://stock.adobe.com/images/reset-button-line-icon-outline-vector-sign-linear-style-pictogram-isolated-on-white-symbol-logo-illustration-editable-stroke-pixel-perfect/152009490
    app.restartButtonImg = openImage("images/restartButton.png")
    app.restartButtonRadius = app.width * 0.03
    app.restartButton = Button(app.width*0.47, app.height * 0.47, 
                               app.width*0.06, app.width*0.06, 'circle')
    app.restartButtonInteracted = False

    # Back Button from https://pngtree.com/freepng/back-vector-icon_3791389.html
    app.backButtonImg = openImage("images/backButton.png")
    app.backButtonRadius = app.width * 0.03
    app.backButton = Button(app.width * 0.47, app.height *0.85, 
                            app.width * 0.06, app.width * 0.06, 'circle')
    app.backButtonInteracted = False

    # pause message
    # word images from https://www.fontspace.com/valorax-font-f89146
    app.pauseMessage = CMUImage(openImage("images/paused.png"))

    # Spike image
    app.spikeImg = openImage("images/spike.png")
    app.spikeImg = CMUImage(app.spikeImg)

    # wall image
    app.wallImg = openImage("images/wall.jpg")

    # player image from https://imgbin.com/png/zwG5NGZw/assam-macaque-monkey-png
    app.playerImg = openImage("images/playerImg.png")

    # player and game initialization 
    app.isSwinging = False
    app.ropeLength = 200
    app.player = Player(app.width*0.4, 200, app.playerImg)

    # start and death menu player
    app.menuPlayer = Player(app.width * 0.9, app.height*0.6, app.playerImg)
    app.menuPlayer.omega = 0
    app.menuPlayer.angle = math.pi

    # pivots
    app.pivots = []
    app.currPivot = None
    app.menuPivot = Pivot(app.width*0.7, app.height * 0.6)

    # walls
    app.walls = []

    # spikes
    app.spikes = []
    
    generateInitialState(app)

    # scrolling 
    app.scrollSpeed = 0
    app.scrollX = 0 
    app.backdropScroll = 0
    app.scrollMargin = 400
    app.isScrolling = False

    # High Score
    app.scores = []

    # color
    app.selectedColor = rgb(255, 228, 181)

#--------------------------------- Start ---------------------------------------
def welcome_redrawAll(app):
    drawImage(app.startMenuBackground, 0, 0, 
              width = app.width, height = app.height)
    drawImage(app.logo, app.width*0.135, app.height*0.1, width = app.width*0.4)
    
    # different color if button is hovered over 
    if app.startButtonInteracted:
        app.startButton.draw(app.startClickedImg)
    else:
        app.startButton.draw(app.startUnclickedImg)

    if app.helpButtonInteracted:
        app.helpButton.draw(app.helpClickedImg)
    else:
        app.helpButton.draw(app.helpUnclickedImg)

    if app.scoresButtonInteracted:
        app.scoresButton.draw(app.scoresClickedImg)
    else:
        app.scoresButton.draw(app.scoresUnclickedImg)
    
    # drawing menu player, rope and pivot 
    drawLine(app.menuPlayer.x, app.menuPlayer.y, app.menuPivot.x, 
             app.menuPivot.y, fill = 'peru', lineWidth = 6, dashes = (15, 3))
    app.menuPlayer.draw()
    app.menuPivot.draw('blue')

def welcome_onStep(app):

    # menu player swinging 
    r = distance(app.menuPlayer.x, app.menuPlayer.y, 
                 app.menuPivot.x, app.menuPivot.y)
    app.menuPlayer.swing(app.menuPivot, r, True, 0)

def welcome_onMousePress(app, mouseX, mouseY):
    if app.startButton.clickedOrHovered(mouseX, mouseY):
        setActiveScreen('game')
        startGame(app)
        app.startButtonInteracted = False
    elif app.helpButton.clickedOrHovered(mouseX, mouseY):
        setActiveScreen("help")
        app.helpButtonInteracted = False
    elif app.scoresButton.clickedOrHovered(mouseX, mouseY):
        setActiveScreen("scores")

        # reading high scores from file 
        with open("scores.txt", "r") as file:
            data = file.read()
        if data.isspace():
            app.scores = []
        else:
            data = data.splitlines()
            for i in range(len(data)):
                if data[i] != '': # only reads scores, not blank lines
                    app.scores.append(int(data[i]))
            app.scores.sort(reverse = True)
        # deselects score button 
        app.scoresButtonInteracted = False

def welcome_onMouseMove(app, mouseX, mouseY):
    if app.startButton.clickedOrHovered(mouseX, mouseY):
        app.startButtonInteracted = True
    else:
        app.startButtonInteracted = False
    if app.helpButton.clickedOrHovered(mouseX, mouseY):
        app.helpButtonInteracted = True
    else:
        app.helpButtonInteracted = False
    if app.scoresButton.clickedOrHovered(mouseX, mouseY):
        app.scoresButtonInteracted = True
    else:
        app.scoresButtonInteracted = False

#--------------------------------- Help ----------------------------------------
def help_redrawAll(app):
    drawImage(app.startMenuBackground, 0, 0, 
              width = app.width, height = app.height)
    drawInstructions(app)

    if app.backButtonInteracted:
        color = app.selectedColor
    else:
        color = 'white'

    # drawing circle 
    drawCircle(app.backButton.left + app.backButtonRadius, 
               app.backButton.top + app.backButtonRadius, 
               app.backButtonRadius, fill = color)
    app.backButton.draw(app.backButtonImg)

def drawInstructions(app):
    drawRect(app.width*0.15, app.height*0.1, app.width*0.7, app.height*0.7, 
             fill = 'white', border = app.selectedColor, borderWidth = 10)
    # instructions message was written on word document and screenshotted
    # size is adjusted to fit the design 
    drawImage(app.instructionsMessage, app.width*0.17, 
              app.height*0.12, width = app.width*0.6, height = app.height*0.66)

def help_onMouseMove(app, mouseX, mouseY):
    if app.backButton.clickedOrHovered(mouseX, mouseY):
        app.backButtonInteracted = True
    else:
        app.backButtonInteracted = False

def help_onMousePress(app, mouseX, mouseY):
    if app.backButton.clickedOrHovered(mouseX, mouseY):
        setActiveScreen("welcome")
        app.backButtonInteracted = False

#-------------------------------- Scores ---------------------------------------
def scores_redrawAll(app):
    drawImage(app.startMenuBackground, 0, 0, 
              width = app.width, height = app.height)
    drawScores(app)
    if app.backButtonInteracted:
        color = app.selectedColor
    else:
        color = 'white'
    drawCircle(app.backButton.left + app.backButtonRadius, 
               app.backButton.top + app.backButtonRadius, 
               app.backButtonRadius, fill = color)
    app.backButton.draw(app.backButtonImg)

def drawScores(app):

    drawRect(app.width*0.15, app.height*0.1, app.width*0.7, app.height*0.7, 
             fill = 'white', border = app.selectedColor, borderWidth = 10)
    if len(app.scores) == 0:
        drawLabel('No high scores yet', app.width/2, 
                  app.height*0.45, size = 35, align='center', 
                  font = 'monospace', italic = True, bold = True)
    i = 0
    while i < len(app.scores) and i < 8 :
        score = app.scores[i]
        drawLabel(f'{i+1}: {score}', app.width*0.43, app.height * 0.2 + 
                  app.height * 0.07 * i, size = 35, align='left', 
                  font = 'monospace', italic = True, bold = True)
        i+=1
def scores_onMouseMove(app, mouseX, mouseY):
    if app.backButton.clickedOrHovered(mouseX, mouseY):
        app.backButtonInteracted = True
    else:
        app.backButtonInteracted = False

def scores_onMousePress(app, mouseX, mouseY):
    if app.backButton.clickedOrHovered(mouseX, mouseY):
        setActiveScreen("welcome")
        app.backButtonInteracted = False

#--------------------------------- Game ----------------------------------------      
def game_onStep(app):

    # death condition
    if (app.player.y - app.player.radius > app.height or 
        app.player.x - app.player.radius < 0):
        setActiveScreen('death')

    # swinging motion 
    if app.isSwinging:
        # check for wall collision
        if checkWallCollision(app.walls, app.player):
            app.player.omega *= -1 # rebounds player
        elif checkSpikeCollision(app.spikes, app.player):
            app.player.dx = 0
            app.player.dy = 0
            app.player.ddx = 0
            app.player.ddy = 0
            time.sleep(1)
            setActiveScreen('death')
        
        app.player.swing(app.currPivot, app.player.ropeLength, 
                         app.isScrolling, app.scrollSpeed, 0.001)
        
        makePlayerVisible(app) 
    
    # freefall motion 
    else: 
        # collision with walls
        collision = checkWallCollision(app.walls, app.player)
        if collision in ['left', 'right']:
            app.player.dx *= -1
        elif collision in ['top', 'bottom']:
            # bouncing off walls from the top or bottom gives a boost 
            app.player.dy *= -1.2

        #collision with spikes
        elif checkSpikeCollision(app.spikes, app.player):
            app.player.dx = 0
            app.player.dy = 0
            app.player.ddx = 0
            app.player.ddy = 0
            time.sleep(1)
            setActiveScreen('death')
    
        app.player.fall(app.isScrolling, app.scrollSpeed)

        makePlayerVisible(app)

    # update positions again for paralax scrolling 
    updatePositions(app)
    
    removePivots(app)
    removeWalls(app)
    removeSpikes(app)

    if len(app.pivots)<5:
        generatePivots(app)
    if len(app.walls)<5: 
        generateWalls(app)
    app.player.x -= app.scrollSpeed

def game_onKeyPress(app, key):
    if key =='p':
        setActiveScreen('pause')
    
    elif key == 'space':
        app.currPivot = app.player.nearestPivot(app.pivots)
        if canSwing(app.player, app.currPivot, app.ropeLength):
            app.isSwinging = True
            app.player.ropeLength = app.player.distance(app.currPivot.x, 
                                                        app.currPivot.y)
            
            # part of momentum is lost when player initially attaches
            angle = app.player.angleToPivot(app.currPivot)
            app.player.angle = angle
            temp = (app.player.dx * math.sin(angle) + app.player.dy 
                    * math.cos(angle))
            app.player.dx = temp * math.sin(angle)
            app.player.dy = temp * math.cos(angle)
            app.player.omega = temp/app.player.ropeLength        

def game_onKeyRelease(app, key):
    if key == 'space' and app.isSwinging:
        app.isSwinging = False
        app.currPivot = None
        # if app.player.angle < math.pi:
        #     app.player.dy -= 1
        app.player.angle = None

def game_redrawAll(app):
    # drawing backdrop
    numBackdrops = math.ceil(app.width / app.backdropWidth) + 1
    newWidth = app.backdropWidth
    newHeight = app.height
    # print(app.backdropScroll)

    for i in range(numBackdrops):
        drawImage(app.backdrop, i*newWidth - app.backdropScroll, 
                  0, width = newWidth, height = newHeight)

    # Scroll   
    drawLabel(f'app.scrollX = {app.scrollX}', app.width/2, 40, fill='white')

    # pivots
    for pivot in app.pivots:
        if pivot is app.currPivot and app.isSwinging:
            # pivot.draw(app.scrollX, 'blue')
            pivot.draw('blue')
        else: 
            # pivot.draw(app.scrollX)
            pivot.draw()
    # obstacles
    for wall in app.walls:
        wall.draw()
    for spike in app.spikes:
        spike.draw()
    # draw rope
    if app.isSwinging:
        drawLine(app.player.x, app.player.y, app.currPivot.x, 
                 app.currPivot.y, fill = 'peru', lineWidth = 6, dashes = (15,3))
    app.player.draw()
#--------------------------------- Pause ---------------------------------------
def pause_onKeyPress(app, key):
    if key=='p':
        setActiveScreen('game')

def pause_redrawAll(app):
    game_redrawAll(app)
    drawImage(app.pauseMessage, app.width * 0.25, app.height*0.45, 
              width = app.width*0.5, height = app.height * 0.1)

#--------------------------------- Death ---------------------------------------
def death_redrawAll(app):
    drawImage(app.startMenuBackground, 0, 0, 
              width = app.width, height = app.height)
    if app.restartButtonInteracted:
        color = app.selectedColor
    else:
        color = 'white'
    drawImage(app.deathMessage, app.width * 0.3, app.height * 0.3, 
              width = app.width * 0.4)
    drawCircle(app.restartButton.left + app.restartButtonRadius, 
               app.restartButton.top + app.restartButtonRadius, 
               app.restartButtonRadius, fill = color)
    app.restartButton.draw(app.restartButtonImg)

def death_onMouseMove(app, mouseX, mouseY):
    if app.restartButton.clickedOrHovered(mouseX, mouseY):
        app.restartButtonInteracted = True
    else:
        app.restartButtonInteracted = False

def death_onMousePress(app, mouseX, mouseY):
    if app.restartButton.clickedOrHovered(mouseX, mouseY):
        setActiveScreen("welcome")
    with open("scores.txt", "a") as file1:
        file1.write(str(int(app.scrollX)) + '\n')

#----------------------------- Helper functions --------------------------------
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def canSwing(player, currPivot, ropeLength):
    distance = ((player.x - currPivot.x)**2 + (player.y- currPivot.y)**2)**0.5
    return distance <= ropeLength

def makePlayerVisible(app):
    # scroll to make player visible as needed
    
    if isScrolling(app): # check to see if player is at margins
        app.isScrolling = True
        app.scrollSpeed = app.player.dx
        app.scrollX += app.scrollSpeed
        app.backdropScroll = app.scrollX % app.backdropWidth
        updatePositions(app)

    # if (app.player.x < app.scrollX + app.scrollMargin):
    #     app.scrollX = app.player.x - app.scrollMargin
    # if (app.player.x > app.scrollX + app.width - app.scrollMargin):
    #     app.scrollX = app.player.x - app.width + app.scrollMargin
    else:
        app.isScrolling = False
        app.scrollSpeed = 0

def checkWallCollision(walls, player):
    for wall in walls:
        collisionSide = wall.collided(player)
        if collisionSide:
            return collisionSide
    return None

def checkSpikeCollision(spikes, player):
    for spike in spikes:
        if spike.collided(player):
            return True
    return False   

def isScrolling(app):
    if (app.player.x > app.width - app.scrollMargin):
        return True
    
def removePivots(app):
    counter = 0
    while counter < len(app.pivots):
        pivot = app.pivots[counter]
        if pivot.x < 0:
            app.pivots.pop(counter)
            print('pivot removed')
        else:
            counter += 1
def removeWalls(app):
    counter = 0
    while counter < len(app.walls):
        wall = app.walls[counter]
        if wall.left + wall.width < 0:
            app.walls.pop(counter)
            print('wall removed')
        else:
            counter += 1
def removeSpikes(app):
    counter = 0
    while counter < len(app.spikes):
        spike = app.spikes[counter]
        if spike.x + spike.r < 0:
            app.spikes.pop(counter)
            print('spike removed')
        else:
            counter += 1

def updatePositions(app):
    for pivot in app.pivots:
        pivot.x -= app.scrollSpeed
    for wall in app.walls:
        wall.left -= app.scrollSpeed
    for spike in app.spikes:
        spike.x -= app.scrollSpeed

def generatePivots(app):
    newPivot = Pivot(randrange(int(1.2*app.width), int(1.3*app.width)), 
                     randrange(int(0.4*app.height), int(0.65 * app.height)))
    app.pivots.append(newPivot)

    prevPivot = app.pivots[-2]
    nextPivot = app.pivots[-1]
    spikeX = randrange(int(prevPivot.x + 0.3*(nextPivot.x - prevPivot.x)), int(prevPivot.x + 0.6*(nextPivot.x - prevPivot.x)))
    spikeY = randrange(int(prevPivot.y - 100), int(prevPivot.y+25))
    spikeR = randrange(30, 40)
    newSpike = Spike(spikeX, spikeY, spikeR, app.spikeImg)
    app.spikes.append(newSpike)

    if nextPivot.y < prevPivot.y: # nextPivot is higher than prevPivot
        wallX = randrange(int(prevPivot.x + (nextPivot.x - prevPivot.x)*0.3), 
                              int(prevPivot.x + (nextPivot.x - prevPivot.x)*0.6))
        wallY = randrange(int(prevPivot.y) + 200, int(prevPivot.y + 300))
        wallWidth = randrange(50, int(nextPivot.x - prevPivot.x))
        wallHeight = randrange(50, 100)
        newWall = Wall(wallX, wallY, wallWidth, wallHeight, app.wallImg)
        app.walls.append(newWall)

def generateWalls(app):
    pass
def generateSpikes(app):
    pass

def openImage(fileName):
    return im.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def generateInitialState(app):
    app.pivots.append(Pivot(randrange(int(app.width*0.46), int(app.width*0.54)), 
                            randrange(int(app.height*0.45), int(app.height*0.55))))
    app.pivots.append(Pivot(randrange(int(app.width*0.75), int(app.width*0.8)), 
                            randrange(int(app.height*0.45), int(app.height*0.55))))
    app.pivots.append(Pivot(randrange(int(app.width*0.9), int(app.width*1.1)), 
                            randrange(int(app.height*0.35), int(app.height*0.55))))
    app.pivots.append(Pivot(randrange(int(app.width*1.2), int(app.width*1.3)), 
                            randrange(int(app.height*0.5), int(app.height*0.6))))
    app.pivots.append(Pivot(randrange(int(app.width*1.45), int(app.width*1.6)), 
                            randrange(int(app.height*0.35), int(app.height*0.55))))

    # wall generation

    for i in range(1, len(app.pivots)):
        prevPivot = app.pivots[i-1]
        nextPivot = app.pivots[i]
        if nextPivot.y < prevPivot.y: # nextPivot is higher than prevPivot
            wallX = randrange(int(prevPivot.x + (nextPivot.x - prevPivot.x)*0.1), 
                              int(prevPivot.x + (nextPivot.x - prevPivot.x)*0.6))
            wallY = randrange(int(prevPivot.y) + 200, int(prevPivot.y + 300))
            wallWidth = randrange(50, int(nextPivot.x-prevPivot.x))
            wallHeight = randrange(50, 100)
            newWall = Wall(wallX, wallY, wallWidth, wallHeight, app.wallImg)
            app.walls.append(newWall)
        
    for i in range(1, len(app.pivots)):
        prevPivot = app.pivots[i-1]
        nextPivot = app.pivots[i]

        spikeX = randrange(int(prevPivot.x + 0.3*(nextPivot.x - prevPivot.x)), int(prevPivot.x + 0.6*(nextPivot.x - prevPivot.x)))
        spikeY = randrange(int(prevPivot.y - 25), int(prevPivot.y + 25))
        spikeR = randrange(30, 40)
        newSpike = Spike(spikeX, spikeY, spikeR, app.spikeImg)
        app.spikes.append(newSpike)

    # app.walls.append(Wall(app.width*0.4, app.height*0.8, 100, 50, app.wallImg))
    # app.walls.append(Wall(app.width*0.6, app.height*0.4, 100, 200, app.wallImg))
    # app.walls.append(Wall(app.width*7/8, app.height*0.8, 100, 50, app.wallImg))
    # app.walls.append(Wall(app.width, app.height*0.3, 50, 50, app.wallImg))

    # app.spikes.append(Spike(app.width*3/4, app.height*3/4, 30, app.spikeImg))
    # app.spikes.append(Spike(app.width*7/8, app.height*0.5, 30, app.spikeImg))

runAppWithScreens(initialScreen='welcome')
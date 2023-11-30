from cmu_graphics import *
from player import *
from obstacle import *
from pivot import *
from button import *

def onAppStart(app):
    startGame(app)

def startGame(app):
    app.width = 1280
    app.height = 720
    app.isSwinging = False
    app.ropeLength = 200
    app.player = Player(app.width/4 + 200, 100)
    app.pivots = []
    app.pivots.append(Pivot(app.width/2, app.height/2))
    app.pivots.append(Pivot(app.width*3/4, app.height/2))
    app.pivots.append(Pivot(app.width, app.height/2))
    app.pivots.append(Pivot(app.width*5/4, app.height/2))
    app.currPivot = None
    app.stepsPerSecond = 60
    app.g = 9.81 / app.stepsPerSecond
    app.startButton = Button(app.width/2 - 100, app.height/2 - 100, 200, 200, 'start')


    app.scrollX = 0 
    app.scrollMargin = 300


#--------------------------------- Start ---------------------------------------
def welcome_redrawAll(app):
    app.startButton.draw()

def welcome_onMousePress(app, mouseX, mouseY):
    if app.startButton.clicked(mouseX, mouseY):
        setActiveScreen('game')
        startGame(app)

#--------------------------------- Game ----------------------------------------

def game_onStep(app):
    if app.player.y - app.player.radius > app.height:
        setActiveScreen('death')

    if app.isSwinging:
        app.player.swing(app.currPivot, app.player.ropeLength)
        makePlayerVisible(app) 
    else: 
        app.player.fall()
        makePlayerVisible(app) 

def makePlayerVisible(app):
    # scroll to make player visible as needed
    if (app.player.x > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = app.player.x - app.width + app.scrollMargin
    # if (app.player.x < app.scrollX + app.scrollMargin):
    #     app.scrollX = app.player.x - app.scrollMargin
    # if (app.player.x > app.scrollX + app.width - app.scrollMargin):
    #     app.scrollX = app.player.x - app.width + app.scrollMargin

def game_onKeyPress(app, key):
    if key =='p':
        setActiveScreen('pause')
    
    elif key == 'space':
        app.currPivot = app.player.nearestPivot(app.pivots)
        if canSwing(app.player, app.currPivot, app.ropeLength):
            app.isSwinging = True
            app.player.ropeLength = app.player.distance(app.currPivot.x, app.currPivot.y)
            print(app.player.highestAngle(app.currPivot, app.player.ropeLength))
            angle = app.player.angleToPivot(app.currPivot)
            app.player.angle = angle
            temp = app.player.dx * math.sin(angle) + app.player.dy * math.cos(angle)
            app.player.dx = temp * math.sin(angle)
            app.player.dy = temp * math.cos(angle)
            app.player.omega = temp/app.player.ropeLength        
            # angle = app.player.highestAngle(app.currPivot, app.player.ropeLength)
            # app.player.amplitude = abs(math.degrees(angle) - (180 - math.degrees(angle)))/2
            # app.player.minAngle = angle
            # app.player.maxAngle = 180 - angle

def game_onKeyRelease(app, key):
    if key == 'space' and app.isSwinging:
        app.isSwinging = False
        app.player.angle = None
        app.currPivot = None
        #if app.player.angle < math.pi:
        #    app.player.vy -= 10
        #app.player.angle = None
        
# def onKeyHold(app, keys):        
#     if 'space' in keys:
#         app.player.swing()  

def game_redrawAll(app):
    app.player.draw(app.scrollX)
    
    drawLabel(f'app.scrollX = {app.scrollX}', app.width/2, 40, fill='black')
    for pivot in app.pivots:
        if pivot is app.currPivot and app.isSwinging:
            pivot.draw(app.scrollX, 'blue')
        else: 
            pivot.draw(app.scrollX)

    if app.isSwinging:
        drawLine(app.player.x-app.scrollX, app.player.y, app.currPivot.x - app.scrollX, app.currPivot.y)

#--------------------------------- Pause ---------------------------------------
def pause_onKeyPress(app, key):
    if key=='p':
        setActiveScreen('game')

def pause_redrawAll(app):
    game_redrawAll(app)
    drawLabel('PAUSED!', app.width/2, 300)

#--------------------------------- Death ---------------------------------------
def death_redrawAll(app):
    drawLabel('YOU DIED!', app.width/2, app.height/2)

def death_onKeyPress(app, key):
    if key == 'r':
        
        setActiveScreen('welcome')

def distance(x1, x2, y1, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def canSwing(player, currPivot, ropeLength):
    distance = ((player.x - currPivot.x)**2 + (player.y- currPivot.y)**2)**0.5
    return distance <= ropeLength

runAppWithScreens(initialScreen='welcome')
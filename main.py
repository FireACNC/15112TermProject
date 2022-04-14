from rotateMaze import *
from spider import *

def onAppStart(app):
    app.row,app.col = 15,15
    app.width = app.height = 800
    app.gridSize = app.width // (app.row + 5)
    app.xmargin = app.ymargin = 2.5*app.gridSize
    app.rotateSpeed = 0
    app.rotateAngle = 0
    app.gridPara = [[0]*app.row for col in range(app.col)]
    app.paused = False
    initMaze(app)
    app.spider = Spider(app,1,1)

def onStep(app):
    if not app.paused:
        doStep(app)

def doStep(app):
    app.spider.update(app)
    rotateMap(app)

def rotateMap(app):
    dAngle = math.radians(app.rotateSpeed)
    app.rotateAngle += dAngle
    app.rotateSpeed /= 1.5
    if abs(app.rotateSpeed) < 1:
        app.rotateSpeed = 0 
    if app.rotateSpeed != 0: storeGrid(app)
    if app.spider.onWall: 
        app.spider.moveWithWall(app,dAngle)

def onKeyHold(app,key):
    if 'a' in key:
        app.rotateSpeed -= 3
    elif 'd' in key:
        app.rotateSpeed += 3

def onMousePress(app,x,y):
    app.spider.cx = x
    app.spider.cy = y
    app.spider.xV, app.spider.yV = 0,0

def onKeyPress(app,event):
    if event == 'p':
        app.paused = not app.paused
    elif event == 's':
        doStep(app)
    if event.isdigit()== True or event == 'r':
        initMaze(app)
    if event == '1':
        btGenerateMaze(app,{(1,1)},(1,1))
    elif event == '2':
        krusGenerateMaze(app,sorted(app.walls))
    elif event == '3':
        primGenerateMaze(app,(1,1))
    elif event == '4':
        wilsonGenerateMaze(app)
    elif event == '5':
        hakGenerateMaze(app)
    elif event == '6':
        ellerGenerateMaze(app)
    elif event == '7':
        recDivGenerateMaze(app)
    elif event == '8':
        binaryGenerateMaze(app)
    elif event == '9':
        sideGenerateMaze(app)
    elif event == 'k':
        doStep(app)
        app.spider.shake(app)
    storeGrid(app)


def redrawAll(app):
    drawGrid(app)
    drawSpider(app)

runApp()
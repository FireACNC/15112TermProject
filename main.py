from rotateMaze import *
from spider import *
from anime import *

def onAppStart(app):
    app.background = 'wheat'
    app.row,app.col = 7,7
    app.width = app.height = 800
    app.paused = False
    app.status = None
    
    app.circleAnime = Anime(app,'Circle')
    app.coverAnime = Anime(app,'Cover')
    initGame(app)

def initGame(app):
    app.gridSize = app.width // (max(app.col,app.row) + 5)
    app.xmargin = (app.width - app.col*app.gridSize)/2
    app.ymargin = (app.height - app.row*app.gridSize)/2
    app.rotateSpeed = 0
    app.rotateAngle = 0
    app.gridPara = [[0]*app.col for row in range(app.row)]

    app.solve = False
    app.sol = []
    app.solPara = []
    app.lock = []
    app.lockPara = []
    app.keys = []
    app.keysPara = []
    initMaze(app)
    #random select algorithm
    mazeIndex = random.randint(0,8)
    if mazeIndex == 0:
        btGenerateMaze(app,{(1,1)},(1,1))
    elif mazeIndex == 1:
        krusGenerateMaze(app,sorted(app.walls))
    elif mazeIndex == 2:
        primGenerateMaze(app,(1,1))
    elif mazeIndex == 3:
        wilsonGenerateMaze(app)
    elif mazeIndex == 4:
        hakGenerateMaze(app)
    elif mazeIndex == 5:
        ellerGenerateMaze(app)
    elif mazeIndex == 6:
        recDivGenerateMaze(app)
    elif mazeIndex == 7:
        binaryGenerateMaze(app)
    elif mazeIndex == 8:
        sideGenerateMaze(app)
    app.spider = Spider(app,1,1,'saddleBrown')


def onStep(app):
    if not app.paused:
        doStep(app)

def doStep(app):
    app.spider.update(app)
    rotateMap(app)
    checkStatus(app)
    levelUp(app)
    findPath(app)

def rotateMap(app):
    dAngle = math.radians(app.rotateSpeed)
    app.rotateAngle += dAngle
    app.rotateSpeed /= 1.5
    if abs(app.rotateSpeed) < 1:
        app.rotateSpeed = 0 
    storeGrid(app)
    if app.spider.onWall: 
        app.spider.moveWithWall(app,dAngle)

def levelUp(app):
    if app.status == 'Load':
        if app.row < 15:
            app.row += 2
            app.col += 2
        initGame(app)
        app.status = 'Over'

def findPath(app):
    app.sol = []
    if app.solve:
        #check is spider in maze
        relx,rely = relPos(app.spider.cx,app.spider.cy,app)
        row,col = pointInMaze(relx,rely,app)
        if 0 < row < app.row and 0 < col < app.col:
            #check if there is lock
            if app.lock != []:
                targetR,targetC = app.keys[0]
            else: targetR,targetC = app.row-1,app.col-2
            app.sol = oneLineSolve(app.maze,[(row,col)],(row,col),(targetR,targetC))[0]
            storeGrid(app)

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
    elif event == 'r':
        initGame(app)
    elif event == 'b':
        app.solve = not app.solve
    elif event == 'l':
        lockMaze(app)

def redrawAll(app):
    drawGrid(app)
    if app.sol != []: drawSol(app)
    drawSpider(app)
    drawKey(app)
    drawAnime(app)


runApp()
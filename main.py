from rotateMaze import *
from spider import *
from anime import *
from gameUI import *
from bomb import *
from media import *

def onAppStart(app):
    app.background = 'wheat'
    app.row,app.col = 9,9
    app.width = app.height = 800
    app.setting = True
    app.status = 'Init'
    app.level = 0
    app.tick = 0
    app.title = 'Spider - No Way Home'
    
    app.circleAnime = Anime(app,'Circle')
    app.coverAnime = Anime(app,'Cover')
    app.mazeIndex = None
    app.mazeTitle = None
    app.lockAndKey = 'Disabled'
    app.double = 'Disabled'
    app.mouseX,app.mouseY = 0,0
    initGame(app)
    loadMedia(app)

def initGame(app):
    app.gridSize = app.width // (max(app.col,app.row) + 5)
    app.xmargin = (app.width - app.col*app.gridSize)/2
    app.ymargin = (app.height - app.row*app.gridSize)/2
    app.rotateSpeed = 0
    app.rotateAngle = 0
    app.gridPara = [[0]*app.col for row in range(app.row)]
    app.allGridPara = {}

    app.solve = False
    app.sol = []
    app.solPara = []
    app.lock = []
    app.lockPara = []
    app.keys = []
    app.keysPara = []
    app.floors = []
    app.floorsPara = []
    app.bombs = []
    app.bombsPara = []
    initMaze(app)
    #random select algorithm
    mazeIndex = random.randint(0,8) if app.mazeIndex == None else app.mazeIndex

    if mazeIndex == 0:
        btGenerateMaze(app,{(1,1)},(1,1))
        app.mazeTitle = 'Recursive Backtracker'
    elif mazeIndex == 1:
        krusGenerateMaze(app,sorted(app.walls))
        app.mazeTitle = "Kruskal's Algorithm"
    elif mazeIndex == 2:
        primGenerateMaze(app,(1,1))
        app.mazeTitle = "Prim's Algorithm"
    elif mazeIndex == 3:
        wilsonGenerateMaze(app)
        app.mazeTitle = "Wilson's Algorithm"
    elif mazeIndex == 4:
        hakGenerateMaze(app)
        app.mazeTitle = "Hunt-and-Kill Algorithm"
    elif mazeIndex == 5:
        ellerGenerateMaze(app)
        app.mazeTitle = "Eller's Algorithm"
    elif mazeIndex == 6:
        recDivGenerateMaze(app)
        app.mazeTitle = "Recursive Division"
    elif mazeIndex == 7:
        binaryGenerateMaze(app)
        app.mazeTitle = "Binary Tree"
    elif mazeIndex == 8:
        sideGenerateMaze(app)
        app.mazeTitle = "Sidewinder Algorithm"
    app.mazeChoice = app.mazeTitle if app.mazeIndex != None else 'Random'

    if app.lockAndKey == 'Enabled': 
        lockMaze(app)

    loadGrid(app)
    storeGrid(app)
    app.spider = Spider(app,1,1,'saddleBrown')


def onStep(app):
    if not app.setting:
        doStep(app)
    checkStatus(app)
    levelUp(app)
    app.tick += 1

def doStep(app):
    app.spider.update(app)
    rotateMap(app)
    findPath(app)
    updateBomb(app)

def rotateMap(app):
    dAngle = math.radians(app.rotateSpeed)
    app.rotateAngle += dAngle
    app.rotateSpeed /= 1.5
    if abs(app.rotateSpeed) < 1:
        app.rotateSpeed = 0 
        app.sound['turn'].pause()
        app.turnPlay = 0
    else:
        app.sound['turn'].play()
    storeGrid(app)
    if app.spider.onWall: 
        app.spider.moveWithWall(app,dAngle)

def levelUp(app):
    if app.status == 'Load':
        if app.spider.alive: app.level += 1
        initGame(app)
        app.status = 'Over'

def findPath(app):
    app.sol = []
    if app.solve and app.floors == [] and app.bombs == []:
        #check is spider in maze
        relx,rely = relPos(app.spider.cx,app.spider.cy,app)
        row,col = pointInMaze(relx,rely,app)
        if 0 < row < app.row and 0 < col < app.col:
            #check if there is key
            if app.keys != []:
                targetR,targetC = app.keys[0]
            else: targetR,targetC = app.row-1,app.col-2
            app.sol = oneLineSolve(app.maze,[(row,col)],(row,col),(targetR,targetC))[0]
            storeGrid(app)

def onKeyHold(app,key):
    if 'a' in key:
        app.rotateSpeed -= 3
    elif 'd' in key:
        app.rotateSpeed += 3

def onMouseMove(app,x,y):
    app.mouseX,app.mouseY = x,y

def onMousePress(app,x,y):
    if app.setting:
        if app.width*0.1 < x < app.width*0.9:
            if abs(y - 8.5*app.height/16)< app.height / 32:
                #change maze size
                app.row += 2
                app.col += 2
                if app.row > 15 or app.col > 15:
                    app.row, app.col = 5,5
                initGame(app)
            elif abs(y - 10*app.height/16)< app.height / 32:
                #switch maze algorithm
                if app.mazeIndex == None: app.mazeIndex = 0
                elif app.mazeIndex >= 8: app.mazeIndex = None
                else: app.mazeIndex += 1
                initGame(app)
            elif abs(y - 11.5*app.height/16)< app.height / 32:
                #change Lock and key
                app.lockAndKey = 'Disabled' if app.lockAndKey != 'Disabled' else 'Enabled'
                initGame(app)
            elif abs(y - 13*app.height/16)< app.height / 32:
                #change bomb
                app.double = 'Disabled' if app.double != 'Disabled' else 'Enabled'
                initGame(app)
        
        if abs(app.mouseX - app.width/2) < app.width*0.1 and (
            abs(app.mouseY - app.height*15/16) < app.height / 32):
            app.setting = not app.setting
    
    else:
        if app.double == 'Enabled':
            placeBomb(app,x,y)


def onKeyPress(app,event):
    if app.level == 0:
        app.status = 'Pass'
        return

    if event == 'escape':
        app.setting = not app.setting
    # elif event == 's':
    #     doStep(app)
    elif event == 'r':
        initGame(app)
    elif event == 's':
        app.solve = not app.solve
    # elif event == 'l':
    #     lockMaze(app)

def redrawAll(app):
    if app.level == 0:
        drawStart(app)
    elif app.setting:
        drawSetting(app)
    else:
        drawGrid(app)
        drawFloors(app)
        drawMazeTitle(app)
        if app.sol != []: drawSol(app)
        drawSpider(app)
        drawKey(app)
        drawBomb(app)

    drawAnime(app)


runApp()
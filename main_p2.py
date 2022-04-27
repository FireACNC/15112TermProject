from cmu_cs3_graphics import *
from cmu_graphics.utils import *
from client import *

def onAppStart(app):
    app.background = gradient('black','grey','silver',start = 'top')
    app.height,app.width = 800, 800
    app.margin = 100
    app.title = 'Bomber!'
    app.waiting = True
    app.row,app.col = 0,0
    app.gridSize = 0
    app.spiderR,app.spiderC = None,None
    app.map = None
    startClient(app)

def onStep(app):
    #do something to refresh redrawAll.
    #process data from queue
    if recvQueue.qsize() > 0:
        info = recvQueue.get()
        processData(app,info)

def onMousePress(app,x,y):
    if app.waiting: return
    clickedRow = int((y-app.margin)//app.gridSize)
    clickedCol = int((x-app.margin)//app.gridSize)

    #see if the cell is in range and has already been clicked.
    #this is in case that map isn't properly sent by the server.
    if 0 <= clickedRow < app.row and 0 <= clickedCol < app.col:
        if app.map[clickedRow][clickedCol] == 0 and (abs(clickedRow-app.spiderR) > 1 or abs(clickedCol-app.spiderC) > 1):
            app.map[clickedRow][clickedCol] = 1
            mouseClickQueue.put((clickedRow,clickedCol))

def redrawAll(app):
    drawTitle(app)
    drawGrid(app)

def drawGrid(app):
    drawRect(app.margin,app.margin,app.width-2*app.margin,app.height-2*app.margin,
        fill = gradient('silver','grey',start = 'center'), border = 'black', borderWidth = 10)
    if app.waiting:
        drawLabel("Get Ready...",app.width/2,app.height/2,size = app.margin/3,
            font = 'mono', bold = True, fill = 'black')
    else:
        for row in range(app.row):
            for col in range(app.col):
                para = getCellBound(app,row,col)
                color = gradient('silver','grey',start = 'center') if app.map[row][col] == 0 else gradient('crimson','darkRed',start = 'center')
                drawRect(*para,fill = color, border = 'black',borderWidth = 5)

        #draw spider
        if app.spiderR == None or app.spiderC == None: return
        if not 0 <= app.spiderR < app.row or not 0 <= app.spiderC <= app.col: return
        para = getCellBound(app,app.spiderR,app.spiderC)
        drawRect(*para,fill = gradient('lime','green',start = 'center'),border = 'gold',borderWidth = 5)

def drawTitle(app):
    drawLabel("DETONATOR!!!",app.width/2,app.margin/2,size = app.margin*0.8,
        font = 'mono', bold = True, fill = 'darkRed')
    instr = ["Green block represent Spider Position"]
    drawLabel("Press to place a bomb",app.width/2,app.height - 3*app.margin/4,size = app.margin/4,
        font = 'mono', bold = True)
    drawLabel("at least one block away from the spider.",app.width/2,app.height - 2*app.margin/4,size = app.margin/4,
        font = 'mono', bold = True)
    drawLabel("Each block can only be bombed once.",app.width/2,app.height - 1*app.margin/4,size = app.margin/4,
        font = 'mono', bold = True)
    pass

runApp()
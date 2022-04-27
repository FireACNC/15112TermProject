def processData(app,data):
    #This try except is used because sometimes the msg received may be formatted
    #wrong because of two batches received at the same time. 
    #Simply ignore that will solve the problem.
    try:
        index = data[0]
        if index == '':
            return
        elif index == 'spider':
            app.spiderR,app.spiderC = map(int,data[1:])
        elif index == 'start':
            app.waiting = False
        elif index == 'end':
            app.waiting = True
        elif index == 'size':
            app.row,app.col = map(int,data[1:])
            resizeMap(app)
        elif index == 'reset':
            resizeMap(app)
    except:
        pass

def resizeMap(app):
    app.gridSize = (app.width-2*app.margin)/app.col
    app.map = [[0]* app.col for row in range(app.row)]

def getCellBound(app,row,col):
    left = app.margin + col * app.gridSize
    top = app.margin + row * app.gridSize
    return left,top,app.gridSize,app.gridSize
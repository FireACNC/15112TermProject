from cmu_cs3_graphics import *
from cmu_graphics.utils import *
import random, time, copy
import math

# generating maze, rotating maze, draw maze & small widgets (lock, key, floor, etc.)

# Methods such as distance and angleTo are used from cmu graphics.
# getCellBound is learned in class, 15112.

def initMaze(app):
    app.maze = [[0]*app.col for row in range(app.row)]
    #The exit
    app.maze[-1][-2] = 1
    #taking even row/col as walls and odd ones as grid
    app.grids = set()
    for row in range(1,app.row,2):
        for col in range(1,app.col,2):
            app.grids.add((row,col))
            app.maze[row][col] = 1
            #grids are default empty
    
    app.walls = set()
    #not including the edges of maze
    for row in range(1,app.row-1):
        for col in range(1,app.col-1):
            if (row,col) not in app.grids and (row%2 != 0 or col%2 != 0): 
                app.walls.add((row,col))

    #faster if the grid is only updated while maze is updated.


################################################################################

#All following methods are learned merely from descriptions in 
#http://www.astrolog.org/labyrnth/algrithm.htm#perfect
#and http://weblog.jamisbuck.org

#some functions, such as nextGridIsValid, 
#are shared between algorithms.

################################################################################

#Recursive backtracker
def btGenerateMaze(app,visited,lastPos):
    #if all grids (odd positions) visited, maze is complete.
    if visited == app.grids: return
    else:
        directions = [(2,0),(-2,0),(0,2),(0,-2)]
        while directions != []:
            drow,dcol = random.choice(directions)
            directions.remove((drow,dcol))
            row,col = lastPos
            newRow,newCol = row+drow,col+dcol
            if nextGridIsValid(app,newRow,newCol,visited):
                visited.add((newRow,newCol))
                app.maze[newRow][newCol] = 1
                app.maze[(row+newRow)//2][(col+newCol)//2] = 1
                btGenerateMaze(app,visited,(newRow,newCol))

def nextGridIsValid(app,row,col,visited):
    if (row,col) in visited: return False
    if not (0 < row < app.row) or not (0 < col < app.col): return False
    return True
    
################################################################################

#Kruskal's Algorithm
def krusGenerateMaze(app,walls,L = None):
    #make sure not have aliase when the function is used several times
    if L is None: 
        #record all the grids, initially in seperate sets
        L =[{grid} for grid in sorted(app.grids)]
    #for the base case, need to check that all grids are in the same set
    #same as only have one set
    if len(L) == 1: return
    else: 
        (row,col) = random.choice(walls)
        walls.remove((row,col))
        if row%2 == 0: 
            #it means it connected two vertical grids
            grid1,grid2 = (row-1,col),(row+1,col)
        else: grid1,grid2 = (row,col-1),(row,col+1)

        for numSet in L:
            if grid1 in numSet:
                set1 = numSet
            if grid2 in numSet:
                set2 = numSet
        #If they are in the same set,  just don't do anything
        if set1 != set2:
            set3 = set1.union(set2)
            L.remove(set1)
            L.remove(set2)
            L.append(set3)
            app.maze[row][col] = 1

        krusGenerateMaze(app,walls,L)

################################################################################

#Prim's Algorithm
def primGenerateMaze(app,grid,visited = None,wallList = None):
    #make sure not have aliase when the function is used several times
    if visited is None: 
        visited = {grid}
        wallList = primFindWall(app,grid)
    if wallList == []:
        return
    else:
        row,col = random.choice(wallList)
        wallList.remove((row,col))
        if row%2 == 0: 
            #it means it connected two vertical grids
            grid1,grid2 = (row-1,col),(row+1,col)
        else: grid1,grid2 = (row,col-1),(row,col+1)

        newGrid = None
        if grid1 not in visited:
            newGrid = grid1
        if grid2 not in visited:
            if newGrid == grid1: 
                primGenerateMaze(app,grid,visited,wallList)
            newGrid = grid2
        if newGrid == None:
            primGenerateMaze(app,grid,visited,wallList)
        else:
            visited.add(newGrid)
            app.maze[row][col] = 1
            wallList += primFindWall(app,newGrid)
            primGenerateMaze(app,grid,visited,wallList)

def primFindWall(app,grid):
    row,col = grid
    walls = []
    for drow,dcol in [(1,0),(-1,0),(0,1),(0,-1)]:
        newRow,newCol = row+drow,col+dcol
        if (0 < newRow < app.row-1) and (0 < newCol < app.col-1): 
            walls.append((newRow,newCol))
    return walls

################################################################################

#Wilson's Algorithm (improved Aldous-Broder)
#It may takes it too long to find the first way, cause exceeding recursion limit
def wilsonGenerateMaze(app,visited = None,lastGrid = None):
    if visited is None:
        #initialize
        grid1 = random.choice(sorted(app.grids))
        visited = {grid1}
        lastGrid = wilsonChoice(visited,app.grids)
    while True:
        try:
            lst = wilsonWalk(app,visited,lastGrid,[lastGrid])
            break
        except:
            continue
    row,col = lastGrid
    visited.add(lastGrid)
    for newRow,newCol in lst[1:]:
        app.maze[(row+newRow)//2][(col+newCol)//2] = 1 
        row,col = newRow,newCol
        visited.add((newRow,newCol))
    #the base case is actually here
    if visited == app.grids: return
    newGrid = wilsonChoice(visited,app.grids)
    wilsonGenerateMaze(app,visited,newGrid)

def wilsonChoice(visited,grids):
    #choose grid that are not visited
    gridlst = sorted(grids.difference(visited))
    return random.choice(gridlst)
    
def wilsonWalk(app,visited,lastGrid,temp):
    #the random walk part has similar rule as the backtracking method,
    if lastGrid in visited:
        return temp
    directions = [(2,0),(-2,0),(0,2),(0,-2)]
    while directions != []:
        drow,dcol = random.choice(directions)
        directions.remove((drow,dcol))
        row,col = lastGrid
        newRow,newCol = row+drow,col+dcol
        if (0 < row < app.row) and (0 < col < app.col):
            if (newRow,newCol) in temp:
                #update the temp, make sure no loop
                i = temp.index((newRow,newCol))
                temp = temp[:i]
            temp.append((newRow,newCol))
            res = wilsonWalk(app,visited,(newRow,newCol),temp)
            if res != None: return res
            temp.pop()

################################################################################

#Hunt-and-Kill algorithm
def hakGenerateMaze(app,visited = None):
    if visited is None:
        #initialize
        lastGrid = linkGrid = random.choice(sorted(app.grids))
        visited = set()
    elif visited == app.grids: return
    else:
        #hunting mode
        lastGrid,linkGrid = hakHunt(app,visited)

    lst = hakWalk(app,visited,lastGrid,[lastGrid])
    row,col = linkGrid
    visited.add(lastGrid)
    for newRow,newCol in lst:
        app.maze[(row+newRow)//2][(col+newCol)//2] = 1 
        row,col = newRow,newCol
        visited.add((newRow,newCol))
    hakGenerateMaze(app,visited)

def hakHunt(app,visited):
    for row in range(1,app.row,2):
        for col in range(1,app.col,2):
            if (row,col) not in visited: 
                for drow,dcol in [(2,0),(-2,0),(0,2),(0,-2)]:
                    if (row+drow,col+dcol) in visited:
                        return (row,col),(row+drow,col+dcol)

def hakWalk(app,visited,lastGrid,temp):
    #the random walk part has similar rule as the backtracking method,
    directions = [(2,0),(-2,0),(0,2),(0,-2)]
    while directions != []:
        drow,dcol = random.choice(directions)
        directions.remove((drow,dcol))
        row,col = lastGrid
        newRow,newCol = row+drow,col+dcol
        if nextGridIsValid(app,newRow,newCol,temp) and (newRow,newCol) not in visited:
            temp.append((newRow,newCol))
            return hakWalk(app,visited,(newRow,newCol),temp)
    return temp

################################################################################

#Eller's Algorithm
def ellerGenerateMaze(app,row = 1,L = None):
    if L is None:
        L = [{(1,col)} for col in range(1,app.col,2)]
    if row == app.row - 2:
        #base case, join every distinct set
        col = 1
        for newCol in range(3,app.col,2):
            for numSet in L:
                if (row,col) in numSet:
                    set1 = numSet
                if (row,newCol) in numSet:
                    set2 = numSet
            if set1 != set2:
                set3 = set1.union(set2)
                L.remove(set1)
                L.remove(set2)
                L.append(set3)
                app.maze[row][(col+newCol)//2] = 1
            col = newCol
        return
    else:
        #horizontal random join
        col = 1
        for newCol in range(3,app.col,2):
            #similar to kruscal
            for numSet in L:
                if (row,col) in numSet:
                    set1 = numSet
                if (row,newCol) in numSet:
                    set2 = numSet
            #If they are in the same set,  just don't do anything
            if set1 != set2:
                if random.randint(0,1) == 1: #50% chance
                    set3 = set1.union(set2)
                    L.remove(set1)
                    L.remove(set2)
                    L.append(set3)
                    app.maze[row][(col+newCol)//2] = 1
            col = newCol
        #vertical random join
        newRow = row+2
        for numSet in L:
            #choice at least one, up to length of set
            setCopy = copy.copy(numSet)
            length = len(numSet)
            for oldRow,oldCol in setCopy:
                if oldRow == newRow: break
                index = random.randint(1,length)
                if index == length:
                    numSet.add((newRow,oldCol))
                    app.maze[newRow-1][oldCol] = 1
                else:
                    L.append({(newRow,oldCol)})
                length -= 1
                numSet.remove((oldRow,oldCol))
        ellerGenerateMaze(app,newRow,L)

################################################################################

#Recursive Division
def recDivGenerateMaze(app):
    #clear all the wall
    for row,col in app.walls: app.maze[row][col] = 1
    divideMaze(app,0,0,(app.row+1)//2,(app.col+1)//2)

def divideMaze(app,left,top,rowNum,colNum):
    if rowNum <= 2 or colNum <= 2:
        return
    else:
        #randomly choose horizontal or vertical devide
        #index = random.randint(0,1)
        #When I applied the 50% choice way, it is actually very likely to spawn
        #many vertical/horizontal long way, so I designed a probably less skewed
        #and less biased method
        index = random.randint(int(colNum/rowNum * 100)-100,int(colNum/rowNum * 100))
        if index <= 50:
            #horizontal
            selRow = random.randint(1,rowNum-2)
            selCol = random.randint(0,colNum-2)
            rowPos = top+2*selRow
            for col in range(left+1,left+2*colNum-2):
                if (col-left-1)//2 != selCol:
                    app.maze[rowPos][col] = 0
            divideMaze(app,left,top,selRow+1,colNum)
            divideMaze(app,left,rowPos,rowNum-selRow,colNum)
        else:
            #vertical
            selRow = random.randint(0,rowNum-2)
            selCol = random.randint(1,colNum-2)
            colPos = left+2*selCol
            for row in range(top+1,top+2*rowNum-2):
                if (row-top-1)/2 != selRow:
                    app.maze[row][colPos] = 0
                else:
                    app.maze[row][colPos] = 1
            divideMaze(app,left,top,rowNum,selCol+1)
            divideMaze(app,colPos,top,rowNum,colNum-selCol)

################################################################################

#Binary Tree
#This is skewed north west
def binaryGenerateMaze(app):
    for row,col in app.grids:
        pos = []
        if 0 < row-2 < app.row: pos.append((-1,0))
        if 0 < col-2 < app.col: pos.append((0,-1))
        if pos == []: continue
        drow, dcol = random.choice(pos)
        app.maze[row+drow][col+dcol] = 1

################################################################################

#Sidewinder Algorithm
def sideGenerateMaze(app):
    for row in range(1,app.row,2):
        if row == 1:
            for col in range(2,app.col-1,2):
                app.maze[row][col] = 1
        else:
            gridList = []
            for col in range(1,app.col,2):
                index = random.randint(0,1)
                gridList.append((row,col))
                if index == 1 and 0 < col + 2 < app.col:
                    app.maze[row][col+1] = 1
                else:
                    gRow,gCol = random.choice(gridList)
                    app.maze[gRow-1][gCol] = 1
                    gridList = []

################################################################################

# Backtrack path solving learned from http://www.astrolog.org/labyrnth/algrithm.htm#perfect
#There are 300 lines for writing maze, but only ONE line for solving all of them!!!
oneLineSolve = lambda maze,path,start,end : [path] if end in path else list(map(lambda L: L if isinstance(L[0],tuple) else L[0],[ans for ans in [oneLineSolve(maze,path+[(start[0]+drow,start[1]+dcol)],(start[0]+drow,start[1]+dcol),end) for drow,dcol in [(-1,0),(0,1),(0,-1),(1,0)] if (start[0]+drow,start[1]+dcol) not in path and (0 < start[0]+drow < len(maze)) and (0 < start[1]+dcol < len(maze[0])) and maze[start[0]+drow][start[1]+dcol] == 1] if ans]))

################################################################################

def drawGrid(app):
    #draw background
    drawImage(app.images['bg'],0,0,width = app.width,height = app.height)

    for row in range(app.row):
        for col in range(app.col):
            grid = app.gridPara[row][col]
            color = grid[-1]
            dAngle = math.degrees(app.rotateAngle)
            if color == 'sienna':
                cx,cy,size = grid[:3]
                drawImage(app.images['wall'],cx,cy,width = size,height = size,align= 'center',rotateAngle = dAngle)
            elif color == None or color == app.background:
                cx,cy,size = grid[:3]
                drawImage(app.images['grid'],cx,cy,width = size,height = size,align= 'center',rotateAngle = dAngle)

def loadGrid(app):
    app.allGridPara = {}
    for angle in range(0,720):
        dangle = math.radians(angle/2)
        paraAtAngle = [[0]*app.col for row in range(app.row)]
        for row in range(app.row):
            for col in range(app.col):
                if app.maze[row][col] == 0:
                    color = 'sienna'
                elif app.maze[row][col] == 1 or 2:
                    color = app.background
                para = getCellBound(app,row,col)
                unit = getUnit(*para,color,app,dangle)
                paraAtAngle[row][col] = unit
                #cx,cy,width,height,color
        app.allGridPara[angle] = paraAtAngle

def storeGrid(app):
    degreeIndex = int(math.degrees(app.rotateAngle)*2)%720
    if degreeIndex in app.allGridPara:
        app.gridPara = app.allGridPara[degreeIndex]
    else:
        app.gridPara = [[0]*app.col for row in range(app.row)]
        for row in range(app.row):
            for col in range(app.col):
                if app.maze[row][col] == 0:
                    color = 'sienna'
                elif app.maze[row][col] == 1:
                    color = app.background
                elif app.maze[row][col] == 2:
                    color = 'gold'
                para = getCellBound(app,row,col)
                unit = getUnit(*para,color,app)
                app.gridPara[row][col] = unit
                #cx,cy,width,height,color
                #color is used as the very beginning version only draw rectangles

    app.solPara = []
    for row,col in app.sol:
        color = 'tan'
        para = getCellBound(app,row,col)
        unit = getUnit(*para,color,app)
        app.solPara.append(unit)

    app.keysPara = []
    for row,col in app.keys:
        color = 'gold'
        para = getCellBound(app,row,col)
        unit = getUnit(*para,color,app)
        app.keysPara.append(unit)

    app.lockPara = []
    for row,col in app.lock:
        color = 'black'
        para = getCellBound(app,row,col)
        unit = getUnit(*para,color,app)
        app.lockPara.append(unit)

    app.floorsPara = []
    for row,col in app.floors:
        color = 'burlyWood'
        para = getCellBound(app,row,col)
        unit = getUnit(*para,color,app)
        app.floorsPara.append(unit)

    app.bombsPara = []
    for bomb in app.bombs:
        row,col = bomb.row, bomb.col
        color = bomb.color
        para = getCellBound(app,row,col)
        unit = getUnit(*para,color,app)
        app.bombsPara.append(unit)

#there is some problem in passing in the parameter... the position of left and top
#are OPPOSITE but that is the only way this code work! No idea what is happening...
def getUnit(left,top,width,height,color,app,angle = None):
    if angle is None: angle = app.rotateAngle
    midx,midy = app.width/2-app.gridSize/2,app.height/2-app.gridSize/2
    dis = distance(left,top,midx,midy)
    dx, dy = left - midx, top - midy
    if dis == 0:
        newx,newy = midx + app.gridSize/2 ,midy + app.gridSize/2
    else:
        chx = 1 if dx == 0 else dx//abs(dx)
        chy = 1 if dy == 0 else dy//abs(dy) 
        dx, dy = abs(dx),abs(dy)
        sinV,cosV = math.asin(dx/dis),math.acos(dy/dis)
        newSin,newCos = sinV + chx*chy*angle, cosV + chx*chy*angle
        newx,newy = midx + chx * math.sin(newSin) * dis + app.gridSize/2, midy + chy * math.cos(newCos) * dis + app.gridSize/2
    return (newy,newx,width,height,color)

def getCellBound(app,row,col):
    left = app.xmargin + col * app.gridSize
    top = app.ymargin + row * app.gridSize
    return top,left,app.gridSize,app.gridSize

def drawSol(app):
    for index in range(len(app.sol)):
        grid = app.solPara[index]
        color = grid[-1]
        drawCircle(*grid[:2],app.gridSize/8,fill = color,
            rotateAngle = math.degrees(app.rotateAngle),align = 'center')

def drawMazeTitle(app):
    for title,rowNum in [(f"Current Maze: {app.mazeTitle}",-1),(f"Maze Solved: {app.level-1}",app.row)]:
        relTitlePos = getCellBound(app,rowNum,app.col//2)
        titlePos = getUnit(*relTitlePos,None,app)[:2]
        drawLabel(title,*titlePos,
            size = app.width/30,font = 'mono',fill = 'black',bold = True, 
            rotateAngle = math.degrees(app.rotateAngle))

    

################################################################################

#lock and key feature
def lockMaze(app):
    app.maze[-1][-2] = 2
    if (app.row-1,app.col-2) not in app.lock:
        app.lock.append((app.row-1,app.col-2)) 
    #add a random key
    gridLst = sorted(app.grids)
    gridLst.remove((1,1))
    app.keys.append(random.choice(gridLst))

def drawKey(app):
    dAngle = math.degrees(app.rotateAngle)
    for key in app.keysPara:
        cx,cy = key[:2]
        drawImage(app.images['key'],cx,cy,width = app.gridSize,height = app.gridSize,align = 'center',rotateAngle = dAngle)
    for lock in app.lockPara:
        cx,cy = lock[:2]
        drawImage(app.images['lock'],cx,cy,width = app.gridSize,height = app.gridSize,align = 'center', rotateAngle = dAngle)

def drawFloors(app):
    #because it is slow to revise the para of all maze, draw floor above instead.
    for floors in app.floorsPara:
        cx,cy,size = floors[:3]
        dAngle = math.degrees(app.rotateAngle)
        drawImage(app.images['grid'],cx,cy,width = size,height = size,align= 'center',rotateAngle = dAngle)
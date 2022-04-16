from cmu_cs3_graphics import *
from cmu_graphics.utils import *
import random, time, copy

#This is a seperate part merely for exploring maze algorithm. Major code is same
#as rotate maze.

# Methods such as distance and angleTo are used from cmu graphics.
# getCellBound is learned in class, 15112.

def onAppStart(app):
    app.row,app.col = 25,25
    app.gridSize = 20
    app.width,app.height = 800,800
    app.margin = 150
    app.title = 'Initialized Maze'
    app.rotateAngle = 0
    initMaze(app)
    
def initMaze(app):
    app.maze = [[0]*app.col for row in range(app.row)]
    app.maze[0][1] = app.maze[-1][-2] = 1

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

    app.path = []

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


#Solve the maze using recursive backtracker!


oneLineSolve = lambda maze,path,start,end : path if end in path else list(map(lambda L: L if isinstance(L[0],tuple) else L[0],[ans for ans in [oneLineSolve(maze,path+[(start[0]+drow,start[1]+dcol)],(start[0]+drow,start[1]+dcol),end) for drow,dcol in [(-1,0),(0,1),(0,-1),(1,0)] if (start[0]+drow,start[1]+dcol) not in path and (0 < start[0]+drow < len(maze)) and (0 < start[1]+dcol < len(maze[0])) and maze[start[0]+drow][start[1]+dcol] == 1] if ans]))

def rbSolveMaze(app,start,end):
    if app.path == []: app.path.append(start)
    if end in app.path: return True
    for drow,dcol in [(-1,0),(0,1),(0,-1),(1,0)]:
        newRow,newCol = start[0]+drow,start[1]+dcol
        if (newRow,newCol) not in app.path and (0 < newRow < app.row) and (0 < newCol < app.col) and app.maze[newRow][newCol] == 1:
            app.path.append((newRow,newCol))
            res = rbSolveMaze(app,(newRow,newCol),end)
            if res: return True
            app.path.pop()
    return False
    



################################################################################


def onKeyPress(app,event):
    if event.isdigit()== True or event == 'r':
        app.title = 'Initialized Maze'
        initMaze(app)
    if event == '1':
        app.title = 'Recursive Backtracker'
        btGenerateMaze(app,{(1,1)},(1,1))
    elif event == '2':
        app.title = "Kruskal's Algorithm"
        krusGenerateMaze(app,sorted(app.walls))
    elif event == '3':
        app.title = "Prim's Algorithm"
        primGenerateMaze(app,(1,1))
    elif event == '4':
        app.title = "Wilson's Algorithm"
        wilsonGenerateMaze(app)
    elif event == '5':
        app.title = "Hunt-and-Kill Algorithm"
        hakGenerateMaze(app)
    elif event == '6':
        app.title = "Eller's Algorithm"
        ellerGenerateMaze(app)
    elif event == '7':
        app.title = "Recursive Division"
        recDivGenerateMaze(app)
    elif event == '8':
        app.title = "Binary Tree"
        binaryGenerateMaze(app)
    elif event == '9':
        app.title = "Sidewinder Algorithm"
        sideGenerateMaze(app)
    elif event == 's':
        rbSolveMaze(app,(0,1),(app.row-1,app.col-2))
    elif event == 'o':
        path = oneLineSolve(app.maze,[(0,1)],(0,1),(app.row-1,app.col-2))[0]
        print(path)

def redrawAll(app):
    drawGrid(app)
    drawTitle(app)
    drawSol(app)

def drawGrid(app):
    for row in range(app.row):
        for col in range(app.col):
            color = 'black' if app.maze[row][col] == 0 else 'white'
            para = getCellBound(app,row,col)
            drawRect(*para,fill = color)

def drawTitle(app):
    drawLabel(app.title,app.width/2,app.margin/2,size = app.margin/2)

def drawSol(app):
    for row,col in app.path:
        top,left = getCellBound(app,row,col)[:2]
        drawCircle(top+app.gridSize/2,left+app.gridSize/2,app.gridSize/4,fill = 'blue')

def getCellBound(app,row,col):
    top = app.margin + col * app.gridSize
    left = app.margin + row * app.gridSize
    return top,left,app.gridSize,app.gridSize

runApp()

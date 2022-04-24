from cmu_cs3_graphics import *
from cmu_graphics.utils import *

class Spider(object):
    def __init__(self,app,row,col,color):
        self.cx, self.cy = app.gridPara[row][col][:2]
        self.row,self.col = 1,1
        self.r = app.gridSize/3
        self.xV,self.yV = 0,0
        self.xAcc,self.yAcc = 0, 0.8
        self.bounce = 0.6
        self.onWall = True
        self.color = color
        self.rotate = 0
        self.alive = True
    
    def update(self,app):
        if not self.alive: return
        oldX,oldY = self.cx,self.cy
        oldRelx,oldRely = relPos(oldX,oldY,app)
        oldRow,oldCol = pointInMaze(oldRelx,oldRely,app)
        self.row,self.col = oldRow,oldCol
        
        #check key collision
        if (oldRow,oldCol) in app.keys:
            app.keys.remove((oldRow,oldCol))
            if app.keys == []:
                lockR,lockC = app.lock.pop()
                app.maze[lockR][lockC] = 1
                app.floors.append((lockR,lockC))
                app.sound['unlock'].play()

        self.xV += self.xAcc
        self.yV += self.yAcc
        self.cx += self.xV
        self.cy += self.yV
        if self.yV > app.gridSize/2: self.yV = app.gridSize/2

        #incase the grid hasn't spawned yet
        if app.gridPara[0][0] == 0: return

        relx,rely = relPos(self.cx,self.cy,app)
        res = self.checkInWall(app,relx,rely)
        if res != set(): 
            #pull back ball
            #Code that works, but sometimes doesn't:
            index = 0
            hit = True
            tempxV,tempyV = self.xV/2,self.yV/2
            while index < 30:
                index += 1
                self.cx -= tempxV
                self.cy -= tempyV
                relx,rely = relPos(self.cx,self.cy,app)
                tempxV /= 2
                tempyV /= 2
                if self.checkInWall(app,relx,rely) != set():
                    if not hit:
                        tempxV *= -1
                        tempyV *= -1
                else:
                    if hit:
                        tempxV *= -1
                        tempyV *= -1

                relx2,rely2 = relPos(self.cx,self.cy,app)
                res2 = self.checkInWall(app,relx2,rely2)
                if res2 != set(): 
                # More developed but still have bug
                    pulAngle = math.radians(angleTo(oldX,oldY,self.cx,self.cy))
                    pulDis = distance(self.cx,self.cy,oldX,oldY)
                    pulRelx, pulRely = abs(pulDis * math.sin(pulAngle)), abs(pulDis * math.cos(pulAngle))
                    validRelx,validRely = pulRelx,pulRely
                    for hitRow,hitCol in res2:
                        #find which side of the ball is inside the wall
                        if hitRow > oldRow:
                            validRely = app.gridSize * hitRow - app.gridSize/2 - oldRely - self.r
                        elif hitRow < oldRow:
                            validRely = oldRely - app.gridSize * hitRow + app.gridSize/2 - self.r
                        if hitCol > oldCol:
                            validRelx = app.gridSize * hitCol - app.gridSize/2 - oldRelx - self.r
                        elif hitCol < oldCol:
                            validRelx = oldRelx - app.gridSize * hitCol + app.gridSize/2 - self.r
                    #use similar triangle, scale should between 0-1
                    minScaley = validRely/pulRely if abs(pulRely) > 0.01 else 1
                    minScalex = validRelx/pulRelx if abs(pulRelx) > 0.01 else 1
                    minScale = max(0,min(minScaley,minScalex,1))
                    newDis = pulDis * minScale
                    self.cx = oldX + newDis * math.sin(pulAngle)
                    self.cy = oldY - newDis * math.cos(pulAngle)
        
            #calculate bounce speed, figure out which side of the wall is hit
            
            bounceAngle = None
            if (oldRow,oldCol+1) in res or (oldRow,oldCol-1) in res:
                bounceAngle = app.rotateAngle % (math.pi)
            else:
                bounceAngle = (math.pi/2+app.rotateAngle) % (math.pi)

            #Thanks my friend Ken for teaching me math XD
            oldxV,oldyV = self.xV, self.yV
            self.xV = -(math.cos(2*bounceAngle)*oldxV + math.sin(2*bounceAngle)*oldyV)
            self.yV = -(math.sin(2*bounceAngle)*oldxV - math.cos(2*bounceAngle)*oldyV)

            self.xV *= self.bounce
            self.yV *= self.bounce
        
        #rotate Spider
        if abs(self.xV > 0.01) and abs(self.yV > 0.01):
            self.rotate -= min(-math.pi/30,max(math.pi/30,self.xV / self.yV // 10))

        if self.cy > app.height and app.status == 'Game':
            app.status = 'Pass'

        relx,rely = relPos(self.cx,self.cy,app)
        res = self.checkInWall(app,relx,rely)
        if res != set(): self.cx,self.cy = oldX,oldY

        
    #check if the ball is in wall        
    def checkInWall(self,app,relx,rely):
        res = set()
        directions = [(0,1),(-1,0),(1,0),(0,-1)]
        #check if circle extreme point touch the wall
        for dx,dy in directions:
            #check the left, right, top, bottom most point of the circle
            row,col = pointInMaze(relx+dx*self.r,rely+dy*self.r,app)
            if 0 <= col <= app.col-1 and 0 <= row <= app.row-1:  
                if app.maze[row][col] != 1: 
                    res.add((row,col))

        #check if wall extreme point touch the circle
        row,col = pointInMaze(relx,rely,app)
        for drow in [-1,0,1]:
            for dcol in [-1,0,1]:
                if 0 <= row+drow <= app.row-1 and 0 <= col+dcol <= app.col-1:  
                    if app.maze[row+drow][col+dcol] != 1:
                        gridcx,gridcy = (col+dcol)*app.gridSize,(row+drow)*app.gridSize,
                        for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
                            cornerx,cornery = gridcx + dx*app.gridSize/2, gridcy + dy*app.gridSize/2
                            if distance(cornerx,cornery,relx,rely) < self.r:
                                res.add((row+drow,col+dcol))

        return res

    def moveWithWall(self,app,dAngle):
        self.rotate += dAngle
        relx,rely = relPos(self.cx,self.cy,app)
        res = self.checkInWall(app,relx,rely)
        if res == set(): return

        dis = distance(self.cx,self.cy,app.width/2,app.height/2)
        angle = angleTo(app.width/2,app.height/2,self.cx,self.cy)
        newAngle = math.radians(angle) + dAngle
        newRelx,newRely = math.sin(newAngle)*dis,-math.cos(newAngle)*dis
        self.cx,self.cy = app.width/2+newRelx,app.height/2+newRely
        pass

def relPos(cx,cy,app):
    #relative to the middle point of the first grid
    firstGrid = app.gridPara[0][0]
    dis = distance(cx,cy,firstGrid[0],firstGrid[1])
    angle = math.radians(angleTo(firstGrid[0],firstGrid[1],cx,cy)) - (app.rotateAngle)
    relx,rely = math.sin(angle)*dis,-math.cos(angle)*dis
    return (relx,rely)

def pointInMaze(relx,rely,app):
    col,row = rounded(relx + app.gridSize/2) // app.gridSize, rounded(rely + app.gridSize/2) // app.gridSize
    return row,col

def drawSpider(app):
    s = app.spider
    angle = math.degrees(s.rotate)

    #hitbox for testing
    # drawCircle(s.cx,s.cy,s.r,fill = 'grey')

    #body
    drawCircle(s.cx,s.cy,s.r/2,fill = 'black')
    #legs
    for leftRight in (-1,1):
        for eachAngle in range(60,60+4*25,25):
            legAngle = angle + leftRight * eachAngle
            dis = s.r
            cx,cy = s.cx+dis*math.sin(math.radians(legAngle)),s.cy-dis*math.cos(math.radians(legAngle))
            drawLine(cx,cy,s.cx,s.cy,fill = 'black',lineWidth = s.r/10)
            
    #eyes
    for eyeAngle in (angle + 25, angle - 25):
        dis = s.r*0.55
        cx,cy = s.cx+dis*math.sin(math.radians(eyeAngle)),s.cy-dis*math.cos(math.radians(eyeAngle))
        drawCircle(cx,cy,s.r/4, fill = 'white', border = 'black',borderWidth = s.r/20)

        if s.alive:
            #movable eyes
            relAngle = math.radians(angleTo(cx,cy,app.mouseX,app.mouseY))
            maxDis = (s.r/4-s.r/9)
            newDis = min(maxDis,distance(cx,cy,app.mouseX,app.mouseY))
            newCenter = (cx + math.sin(relAngle)*newDis,cy - math.cos(relAngle)*newDis)
            drawCircle(*newCenter,s.r/9, fill = 'black')
        else:
            drawLabel('x',cx,cy,size = s.r/2,bold = True,rotateAngle = angle)
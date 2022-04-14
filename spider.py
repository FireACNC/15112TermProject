from cmu_cs3_graphics import *
from cmu_graphics.utils import *

class Spider(object):
    def __init__(self,app,row,col):
        self.cx, self.cy = app.gridPara[row][col][:2]
        self.r = app.gridSize//4
        self.xV,self.yV = 0,0
        self.xAcc,self.yAcc = 0, 1
        self.bounce = 0.6
        self.onWall = True
        self.isBounce = False
    
    def update(self,app):
        oldX,oldY = self.cx,self.cy
        oldRelx,oldRely = relPos(oldX,oldY,app)
        oldRow,oldCol = pointInMaze(oldRelx,oldRely,app)

        self.xV += self.xAcc
        self.yV += self.yAcc
        self.cx += self.xV
        self.cy += self.yV
        if self.yV > app.gridSize/2: self.yV = app.gridSize/2

        #incase the grid hasn't spawned yet
        if app.gridPara[0][0] == 0: return

        relx,rely = relPos(self.cx,self.cy,app)
        res = self.checkInWall(app,relx,rely)
        if res == set(): 
            return

        #pull back ball
        #Code that works, but sucks:
        index = 0
        hit = True
        tempxV,tempyV = self.xV/2,self.yV/2
        while index < 20:
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
        if res2 == set(): 
            self.isBounce = False
        else:
            self.isBounce = True
            #Plan A doesn't work! Let's go plan B
            #Actually, they worked differently and may help each other.

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
            #use similar triangle
            minScaley = validRely/pulRely if abs(pulRely) > 0.01 else 1
            minScalex = validRelx/pulRelx if abs(pulRelx) > 0.01 else 1
            minScale = min(minScaley,minScalex,1)
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
        
    #check if the ball is in wall        
    def checkInWall(self,app,relx,rely):
        res = set()
        for dx,dy,dir in [(0,1,'Bot'),(-1,0,'Left'),(1,0,'Right'),(0,-1,'Top')]:
            #check the left, right, top, bottom most point of the circle
            row,col = pointInMaze(relx+dx*self.r,rely+dy*self.r,app)
            if 0 <= col <= 14 and 0 <= row <= 14:  
                if app.maze[row][col] == 0: 
                    res.add((row,col))
        return res

    def moveWithWall(self,app,dAngle):
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
    drawCircle(s.cx,s.cy,s.r,fill = 'blue')
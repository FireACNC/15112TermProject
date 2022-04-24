from rotateMaze import *
from spider import *

class Bomb(object):
    def __init__(self,row,col):
        self.row, self.col = row,col
        self.tick = 60
        self.color = 'black'
        self.half = self.tick
        self.colorTick = 0
        self.exploded = False
        self.explodeTick = 15
    
    def update(self):
        if not self.exploded:
            if self.tick == self.half:
                self.color = 'darkRed'
                self.half = self.tick//1.3
                self.colorTick = 0
            elif self.color == 'darkRed':
                self.colorTick += 1
                if self.colorTick == 2:
                    self.color = 'black'
                    self.colorTick = 0
            if self.tick == 1:
                self.exploded = True
                self.tick = self.explodeTick + 1
        self.tick -= 1

    def __eq__(self,other):
        return type(self) == type(other) and (self.row,self.col,self.tick,self.exploded) == (other.row,other.col,other.tick,other.exploded)

def placeBomb(app,x,y):
    relx,rely = relPos(x,y,app)
    brow,bcol = pointInMaze(relx,rely,app)
    if not 0<=brow<app.row or not 0<=bcol<app.col: return
    if abs(brow-app.spider.row) <= 1 and abs(bcol-app.spider.col) <= 1: return
    app.bombs.append(Bomb(brow,bcol))
    app.maze[brow][bcol] = 0
    app.sound['countdown'].play()

def updateBomb(app):
    for bomb in app.bombs: 
        bomb.update()
        if bomb.exploded and bomb.tick == bomb.explodeTick:
            brow,bcol = bomb.row, bomb.col
            for drow in (-1,0,1):
                for dcol in (-1,0,1):
                    nrow,ncol = brow+drow,bcol+dcol
                    if 0<nrow<app.row-1 and 0<ncol<app.col-1:
                        app.maze[nrow][ncol] = 1
                        app.floors.append((nrow,ncol))
                    if app.spider.row == nrow and app.spider.col == ncol:
                        app.status = 'Pass'
                        app.spider.alive = False
            app.sound['countdown'].pause()
            app.sound['explode'].play()
        if bomb.tick <= 0:
            pos = app.bombs.index(bomb)
            app.bombs.pop(pos)
            app.bombsPara.pop(pos)
            brow,bcol = bomb.row, bomb.col

def drawBomb(app):
    for i in range(min(len(app.bombs),len(app.bombsPara))):
        bomb = app.bombsPara[i]
        bombOb = app.bombs[i]
        color = bomb[-1]
        r = app.gridSize/2
        cx,cy = bomb[:2]
        if not bombOb.exploded:
            angle = math.radians(math.degrees(app.rotateAngle)-30)
            drawCircle(cx,cy,r/1.2,fill = color,rotateAngle = math.degrees(app.rotateAngle),align = 'center')
            dis = r / 2.5
            posx, posy = cx + dis * math.sin(angle), cy - dis * math.cos(angle)
            drawCircle(posx,posy,r/3,fill = gradient('white',color,start = 'center'))
        else:
            drawCircle(cx,cy,r*(bombOb.tick/bombOb.explodeTick * 2.5), 
                fill = gradient('white','white','yellow',start = 'center'),border = 'red',
                borderWidth = r/10)
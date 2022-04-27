from cmu_cs3_graphics import *

#Just short for animation (and I because like Anime)
class Anime(object):
    def __init__(self,app,name):
        self.name = name
        self.tick = 0
        self.cx,self.cy = None,None

    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self,other):
        return type(self) == type(other) and self.name == other.name

def checkStatus(app):

    if app.status == 'Pass':
        if app.circleAnime.tick == 0:
            if app.level == 0:
                app.circleAnime.cx,app.circleAnime.cy = 620,220
            else:
                app.circleAnime.cx,app.circleAnime.cy = app.spider.cx,app.spider.cy
            app.sound['ding'].play()
        app.circleAnime.tick += 1
        app.coverAnime.tick += 1
        if app.coverAnime.tick >= int(100/1.2):
            app.status = 'Load'
            app.circleAnime.tick = 0

    #load change to over at levelup
    elif app.status == 'Over':
        app.coverAnime.tick -= 1
        if app.coverAnime.tick <= 0:
            app.status = 'Game'
        
def drawAnime(app):
    #draw the circle anime
    cover = app.coverAnime
    if cover.tick != 0:
        drawRect(0,0,app.width,app.height,fill = app.background,opacity = min(100,cover.tick * 1.2))
    circle = app.circleAnime
    if circle.tick != 0:
        drawCircle(circle.cx,circle.cy,circle.tick**1.1 *10,fill = None, border = 'gold',borderWidth = 7)

################################################################################

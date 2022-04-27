from cmu_cs3_graphics import *
from cmu_graphics.utils import *
import math

#draw start screen
def drawStart(app):
    drawImage(app.images['cover'],0,0,width = app.width,height = app.height)

    #draw a super big spider
    angle = 30
    scx,scy,sr = 620,220,200 #specifically for 800*800

    drawImage(app.images['spider'],scx,scy,width = 200, height = 200, rotateAngle = angle,align = 'center')

    #eyes
    for eyeAngle in (angle + 50, angle - 50):
        dis = sr*0.22
        cx,cy = scx+dis*math.sin(math.radians(eyeAngle)),scy-dis*math.cos(math.radians(eyeAngle))
        #movable eyes
        relAngle = math.radians(angleTo(cx,cy,app.mouseX,app.mouseY))
        maxDis = sr*0.1
        newDis = min(maxDis,distance(cx,cy,app.mouseX,app.mouseY))
        newCenter = (cx + math.sin(relAngle)*newDis,cy - math.cos(relAngle)*newDis)
        drawCircle(*newCenter,sr/20, fill = 'black')

    alphaIndex = 2*abs(50-app.tick % 100)
    drawLabel('Press Any Key To Start',app.width/2,app.height*0.95,
        size = app.height*0.05, font = 'mono', fill = 'sienna',
        bold = True, opacity = alphaIndex )

#setting window: instructions + choose feature
def drawSetting(app):
    drawLabel('Instructions',app.width/2,app.height/15,size = app.height/20,
            font = 'mono', fill = 'sienna', bold = True)
    instructions = [
        'Press A and D to spin the maze',
        'Press R to restart current level',
        'Press S to enable path finder',
        'Press Esc to get here',
    ]
    if app.double == 'Enabled':
        instructions[2] = 'Play with Your Friend!'
    for i in range(len(instructions)):
        text = instructions[i]
        drawLabel(text,app.width/2,(i+2)*app.height/15,size = app.height/30,
            font = 'mono', fill = 'sienna')

    drawLabel('Settings',app.width/2,7*app.height/16,size = app.height/20,
            font = 'mono', fill = 'sienna', bold = True)

    settings = [
        f'Maze Size: {app.row}x{app.col}',
        f'Maze Algorithm: {app.mazeChoice}',
        f'Lock & Key: {app.lockAndKey}',
        f'Bombs: {app.double}'
    ]
    for i in range(len(settings)):
        text = settings[i]
        color = None
        if abs(app.mouseX - app.width/2) < app.width*0.4 and (
            abs(app.mouseY - (1.5*i+8.5)*app.height/16) < app.height / 32):
            color = 'burlyWood'
        drawRect(app.width/2,(1.5*i+8.5)*app.height/16,app.width*0.8,app.height/16,
            align = 'center', fill = color, border = 'sienna', borderWidth = 5)
        drawLabel(text,app.width/2,(1.5*i+8.5)*app.height/16,size = app.height/30,
            font = 'mono', fill = 'sienna')

    color = None
    if abs(app.mouseX - app.width/2) < app.width*0.1 and (
            abs(app.mouseY - app.height*15/16) < app.height / 32):
            color = 'burlyWood'
    drawRect(app.width/2,app.height*15/16,app.width*0.2,app.height/16,
        align = 'center', fill = color, border = 'sienna', borderWidth = 5)
    drawLabel('Done',app.width/2,app.height*15/16,size = app.height/30,
            font = 'mono', fill = 'sienna')
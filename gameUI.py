from cmu_cs3_graphics import *
from cmu_graphics.utils import *
import math

#draw start screen
def drawStart(app):
    #border
    drawRect(0,0,app.width,app.height,fill = None, border = 'sienna', borderWidth = app.gridSize/3)

    #title
    sizeIndex = max(app.width,app.height)/5
    midx,midy = app.width/2,app.height/2
    drawLabel('Spider:',midx - 0.8*sizeIndex, midy - 0.45*sizeIndex,
        font = 'mono',size = sizeIndex*0.7,rotateAngle = -10,fill = 'sienna',bold = True)
    drawLabel('No Way Home',midx + sizeIndex*0.1, midy + 0.15*sizeIndex,
        font = 'mono',size = sizeIndex*0.5,rotateAngle = -10,fill = 'sienna',bold = True)
    
    #draw a super big spider
    angle = 30
    scx,scy,sr = 570,220,130 #specifically for 800*800

    #body
    drawCircle(scx,scy,sr/2,fill = 'black')
    #legs
    for leftRight in (-1,1):
        for eachAngle in range(60,60+4*25,25):
            legAngle = angle + leftRight * eachAngle
            dis = sr
            cx,cy = scx+dis*math.sin(math.radians(legAngle)),scy-dis*math.cos(math.radians(legAngle))
            drawLine(cx,cy,scx,scy,fill = 'black',lineWidth = sr/10)
            
    #eyes
    for eyeAngle in (angle + 25, angle - 25):
        dis = sr*0.55
        cx,cy = scx+dis*math.sin(math.radians(eyeAngle)),scy-dis*math.cos(math.radians(eyeAngle))
        drawCircle(cx,cy,sr/4, fill = 'white', border = 'black',borderWidth = sr/20)

        #movable eyes
        relAngle = math.radians(angleTo(cx,cy,app.mouseX,app.mouseY))
        maxDis = (sr/4-sr/9)
        newDis = min(maxDis,distance(cx,cy,app.mouseX,app.mouseY))
        newCenter = (cx + math.sin(relAngle)*newDis,cy - math.cos(relAngle)*newDis)
        drawCircle(*newCenter,sr/9, fill = 'black')

    alphaIndex = 2*abs(50-app.tick % 100)
    drawLabel('Press Any Key To Start',app.width/2,app.height*0.9,
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
    for i in range(len(instructions)):
        text = instructions[i]
        drawLabel(text,app.width/2,(i+2)*app.height/15,size = app.height/30,
            font = 'mono', fill = 'sienna')

    drawLabel('Settings',app.width/2,7*app.height/16,size = app.height/20,
            font = 'mono', fill = 'sienna', bold = True)

    settings = [
        f'Maze Size: {app.row}x{app.col}',
        f'Maze Algorithm: {app.mazeChoice}',
        f'Lock & Key: {app.lockAndKey}'
    ]
    for i in range(len(settings)):
        text = settings[i]
        color = None
        if abs(app.mouseX - app.width/2) < app.width*0.4 and (
            abs(app.mouseY - (1.5*i+8.5)*app.height/16) < app.height / 32):
            color = 'tan'
        drawRect(app.width/2,(1.5*i+8.5)*app.height/16,app.width*0.8,app.height/16,
            align = 'center', fill = color, border = 'sienna', borderWidth = 5)
        drawLabel(text,app.width/2,(1.5*i+8.5)*app.height/16,size = app.height/30,
            font = 'mono', fill = 'sienna')

    color = None
    if abs(app.mouseX - app.width/2) < app.width*0.1 and (
            abs(app.mouseY - app.height*14/16) < app.height / 32):
            color = 'tan'
    drawRect(app.width/2,app.height*14/16,app.width*0.2,app.height/16,
        align = 'center', fill = color, border = 'sienna', borderWidth = 5)
    drawLabel('Done',app.width/2,app.height*14/16,size = app.height/30,
            font = 'mono', fill = 'sienna')
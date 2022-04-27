from cmu_cs3_graphics import *
from cmu_graphics.utils import *

#This file is used for testing physical movement of ball

def onAppStart(app):
    app.width, app.height = 800,800
    app.mazeCx, app.mazeCy = app.width/2,app.height/2
    app.mazeW, app.mazeH , app.mazeEdge= 250,750,5
    app.margin,app.mazeRotate = 10,0
    app.bounce, app.fraction = 0.8, 0.9
    app.ballCx, app.ballCy, app.ballR = app.mazeCx, app.mazeCy, 10
    app.ballyV, app.ballyAcc = 0, 0.6
    app.ballxV, app.ballxAcc = 0, 0
    app.paused = False
    app.rotateSpeed = 0

    app.tempx,app.tempy = 0,0
    pass

def onStep(app):
    if not app.paused:
        doStep(app)

def doStep(app):
    app.ballyV += app.ballyAcc
    app.ballCy += app.ballyV 
    app.ballxV += app.ballxAcc
    app.ballCx += app.ballxV
    checkInEdge(app)

def checkInEdge(app):
     #check if ball touch edge of rect
    relAngle = math.radians(angleTo(app.mazeCx, app.mazeCy, app.ballCx, app.ballCy))
    angle = relAngle - math.radians(app.mazeRotate)
    dis = distance(app.ballCx,app.ballCy,app.mazeCx,app.mazeCy)
    relx, rely = abs(dis * math.sin(angle)), abs(dis * math.cos(angle))
    maxRelX, maxRelY = (app.mazeW/2 - app.mazeEdge - app.ballR),(
        app.mazeH/2 - app.mazeEdge - app.ballR)

    if relx <= maxRelX and rely <= maxRelY:
        pass
    else:
        #Pull back ball
        newrelx = min(relx,maxRelX)
        newrely = min(rely,maxRelY)
        newDis = math.sqrt(newrelx**2 + newrely**2)
        if 0 < angle%math.pi < math.pi/2:
            newRelAngle = relAngle - (math.atan(relx/rely)-math.atan(newrelx/newrely))
        else:
            newRelAngle = relAngle + (math.atan(relx/rely)-math.atan(newrelx/newrely))
        app.ballCx = app.mazeCx + newDis * math.sin(newRelAngle)
        app.ballCy = app.mazeCy - newDis * math.cos(newRelAngle)

        surfaceDeterAngle = math.atan(maxRelX/maxRelY)
        angle = angle % (2*math.pi)
        if surfaceDeterAngle < angle <= math.pi - surfaceDeterAngle:
            bounceAngle = app.mazeRotate%180
            hitAngle = app.mazeRotate%360
            hitDirect = ((angle - surfaceDeterAngle)/(math.pi - 2*surfaceDeterAngle)-0.5)*2
        elif math.pi - surfaceDeterAngle < angle <= math.pi + surfaceDeterAngle:
            bounceAngle = (90 + app.mazeRotate)%180
            hitAngle = app.mazeRotate%360 + 90
            hitDirect = ((angle - (math.pi - surfaceDeterAngle))/(2*surfaceDeterAngle)-0.5)*2
        elif math.pi + surfaceDeterAngle < angle <= 2* math.pi - surfaceDeterAngle:
            bounceAngle = app.mazeRotate%180
            hitAngle = app.mazeRotate%360 + 180
            hitDirect = ((angle - (math.pi + surfaceDeterAngle))/(math.pi- 2*surfaceDeterAngle)-0.5)*2
        else:
            bounceAngle = (90 + app.mazeRotate)%180
            hitAngle = app.mazeRotate%360 + 270
            if angle < math.pi:
                hitDirect = (angle/(2*surfaceDeterAngle)-0.5)*2
            else:
                hitDirect = ((angle - (2*math.pi - surfaceDeterAngle))/(math.pi)-0.5)*2
        bounceAngle = math.radians(bounceAngle)
        hitAngle = math.radians(hitAngle)

        #Thanks my friend Ken for teaching me math XD
        oldxV,oldyV = app.ballxV, app.ballyV
        app.ballxV = -(math.cos(2*bounceAngle)*oldxV + math.sin(2*bounceAngle)*oldyV)
        app.ballyV = -(math.sin(2*bounceAngle)*oldxV - math.cos(2*bounceAngle)*oldyV)

        #Add the speed of the box
        boxSpeed = dis * math.radians(app.rotateSpeed)
        app.ballxV += boxSpeed * hitDirect * math.cos(hitAngle)
        app.ballyV += boxSpeed * hitDirect * math.sin(hitAngle)
        
        app.ballxV *= app.bounce
        app.ballyV *= app.bounce


def onMousePress(app,eventX,eventY):
    app.ballxV,app.ballyV = 0,0
    app.ballCx, app.ballCy = eventX,eventY
    pass

def onKeyPress(app,key):
    if key == 'p':
        app.paused = not app.paused
    if key == 's':
        doStep(app)

def onKeyHold(app,key):
    if 'a' in key:
        app.mazeRotate -= 1
        app.rotateSpeed = 1
    elif 'd' in key:
        app.mazeRotate += 1
        app.rotateSpeed = -1

def onKeyRelease(app,key):
    app.rotateSpeed = 0

def redrawAll(app):
    # drawCircle(200,200,200,fill = 'white',border = 'black',borderWidth = 5)
    drawRect(app.mazeCx, app.mazeCy,app.mazeW,app.mazeH,fill = 'white',
        border = 'black',borderWidth = app.mazeEdge,
        rotateAngle = app.mazeRotate,align = 'center')
    drawCircle(app.ballCx, app.ballCy, app.ballR, fill = 'blue')
    try:
        drawLine(app.ballCx,app.ballCy,app.ballCx+app.tempx,app.ballCy+app.tempy)
    except:
        pass
    pass

runApp()
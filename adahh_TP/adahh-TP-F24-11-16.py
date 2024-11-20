from cmu_graphics import *
import random
import time
# level clicked on in terms of rows and cols = (row * app.cols) + col

# to fix:
# rotating on falling down and bouncing down, falling down for whenever (falling down fixed)
# ask about lag time with importing an image and how to have multiple lines of 
# text in one drawLabel
# can't jump on game over

# to add:
# - how to win level, set time, if you make it for _ amount of time app.victory
# - levels, each level ups app.stepsPerSecond += 1 and each 10th level gets _ seconds longer
# - when you win a level, the next one gets added to options on menu screen
# - customizable character menu: colors, expressions
# - game over screen
# - accessing side menu (should it return you to same point or reset level? or have choices?)
# - paused screen
# - record per level
# - percentage, completion bar on top of screen that fills in
# - music for pop-up screens and each level

def onAppStart(app):
    app.levels = 10
    app.currentLevel = 1
    app.menu = True
    reset(app)

def reset(app):
    app.starting = True
    # game set-up
    app.stepsPerSecond = 20
    app.width = 600
    app.height = 600
    app.count = 0
    app.pieceShift = 5

    # screen options
    app.paused = False
    app.gameOver = False
    app.options = False
    app.victory = False
    
    # ground
    app.groundTopEdge = int(app.height * 0.75)
    app.groundHeight= int(app.height*0.25)
    app.groundLeftEdge = 0
    app.groundWidth = app.width


    # square
    app.squareWidth = 40
    app.squareTopEdge = app.groundTopEdge-(app.squareWidth)
    app.squareLeftEdge = app.width//2 - app.squareWidth//2
    app.squareBottomEdge = app.groundTopEdge
    app.squareCenter = (app.squareLeftEdge + app.squareWidth//2,
                        app.squareTopEdge + app.squareWidth//2)
    app.bounceHeight = app.squareWidth + app.squareWidth//2
    app.bouncePerStep = 10
    app.bounceSquareUp = False
    app.bounceSquareDown = False
    app.squareRotation = 0
    app.squareRotatePerStep = int(90/(app.bounceHeight//app.bouncePerStep))

    # current objects
    app.onScreen = [(app.groundLeftEdge, app.groundTopEdge, app.groundWidth, app.groundHeight)]
    app.inRangeTopEdge = [app.onScreen[0][1]]

    # menu
    app.offBlack=rgb(52, 46, 55)
    # app.url = 'https://creazilla-store.fra1.digitaloceanspaces.com/icons/3232390/menu-icon-md.png'
    app.startButtonWidth = app.width//5
    app.startButtonHeight = app.height//10
    app.startButtonLeftEdge = app.width//2 - app.startButtonWidth//2
    app.startButtonTopEdge = app.height * 0.8

    app.rows, app.cols = 4,5
    app.getCellSize = (min(app.width,app.height)//(max(app.rows, app.cols)*2 + 1), min(app.width,app.height)//(max(app.rows, app.cols)*2 + 1))

    #sideMenu
    app.imageWidth, app.imageHeight = 20, 20
    app.sideMenuLines = 3
    app.sideMenuLeftEdge, app.sideMenuTopEdge = app.width//100, app.height//100 + (app.height//50)
    app.sideMenuWidth = app.width//15 - app.width//100
    app.sideMenuHeight = (app.sideMenuLines - 1) * app.height//50
    

    # options
    app.optionsWidth = app.width//2
    app.optionsHeight = app.height//2
    app.optionsLeftEdge, app.optionsTopEdge = app.width*0.25, app.height*0.25

    app.homeButtonWidth = app.optionsWidth//5
    app.homeButtonHeight = app.optionsHeight//10
    app.homeButtonLeftEdge = app.optionsLeftEdge + app.optionsWidth//2 - app.homeButtonWidth//2
    app.homeButtonTopEdge = app.optionsTopEdge + app.optionsHeight * 0.8

    # paused
    app.pausedWidth = app.width//2
    app.pausedHeight = app.height//2
    app.pausedLeftEdge, app.pausedTopEdge = app.width*0.25, app.height*0.25

def redrawAll(app):
    
    if app.menu:
        drawMenu(app)
        return
    drawSideMenu(app)
    drawLabel(f'Current Level: {app.currentLevel}', app.width*0.7, app.height * 0.1, align='left')
    drawGround(app)
    drawSquare(app)
    drawPieces(app)
    if app.starting == True:
        drawStartPrompt(app)
    if app.paused:
        drawPaused(app)
    if app.options == True:
        drawOptions(app)

def drawPaused(app):
    drawRect(app.pausedLeftEdge, app.pausedTopEdge, app.pausedWidth, app.pausedHeight, 
             fill=app.offBlack, border = 'black', borderWidth = 4)
    drawLabel('PAUSED', app.width//2, app.pausedTopEdge + app.pausedHeight*0.1, 
              size= app.width*0.5//10, font='monospace', bold=True, fill='darkMagenta', 
              align='center')
    # add how to resume, current level progress, restart button
    

def drawStartPrompt(app):
    cx = app.width//2
    cy = app.groundHeight
    drawLabel("press 'space' to begin...", cx, cy, fill='black', font='monospace',
              bold=True, size=app.width//20)

def drawOptions(app):
    drawRect(app.optionsLeftEdge, app.optionsTopEdge, app.optionsWidth, app.optionsHeight, 
             fill=app.offBlack, border = 'black', borderWidth = 4)
    drawLabel('OPTIONS', app.width//2, app.optionsTopEdge + app.optionsHeight*0.1, 
              size= app.width*0.5//10, font='monospace', bold=True, fill='darkMagenta', 
              align='center')
    #return to homescreen/menu
    drawRect(app.homeButtonLeftEdge, app.homeButtonTopEdge, app.homeButtonWidth,
             app.homeButtonHeight, border='darkMagenta', borderWidth = 4, 
             fill=None)
    drawLabel('HOME', app.homeButtonLeftEdge + app.homeButtonWidth//2, 
              app.homeButtonTopEdge + app.homeButtonHeight//2, fill='darkMagenta', 
              size= app.homeButtonWidth//5, font='monospace', bold=True, align= 'center')
    pass

def drawSideMenu(app):
    for i in range (1,app.sideMenuLines + 1):
        x0, y0 = app.width//100, app.height//100 + (i*app.height//50)
        x1, y1 = app.width//15, app.height//100 + (i*app.height//50)
        drawLine(x0, y0, x1, y1)
    # drawImage(app.load, 0, 0, width=app.imageWidth, height=app.imageHeight)
    

def getButton(app, x, y):
    if getLevel(app, x, y) != None:
        if getLevel(app, x, y) <= app.levels:
            return getLevel(app, x, y)
    if (app.startButtonLeftEdge <= x <= app.startButtonLeftEdge + app.startButtonWidth and
        app.startButtonTopEdge <= y <= app.startButtonTopEdge + app.startButtonWidth):
        return 'start'
    if (app.sideMenuLeftEdge <= x <= app.sideMenuLeftEdge + app.sideMenuWidth and 
        app.sideMenuTopEdge <= y <= app.sideMenuTopEdge + app.sideMenuHeight):
        return 'options'
    if (app.homeButtonLeftEdge <= x <= app.homeButtonLeftEdge + app.homeButtonWidth and
        app.homeButtonTopEdge <= y <= app.homeButtonTopEdge + app.homeButtonHeight):
        return 'home'
    
def getLevel(app, x, y):
    cellWidth, cellHeight = app.getCellSize
    levelsLeft, levelsTop = getCellLeftTop(app, 0, 0)
    levelsRight, levelsBottom = getCellLeftTop(app, app.rows-1, app.cols-1)
    levelsRight, levelsBottom = levelsRight + cellWidth, levelsBottom + cellHeight
    if x < levelsLeft or x > levelsRight:
        return None
    if y < levelsTop or y > levelsBottom:
        return None
    col = ((x - levelsLeft) // (2 * cellWidth)+ 1)
    row = ((y - levelsTop) // (1.5 * cellHeight))
    if isEmpty(app, x, y, row, col-1):
        return None
    return int(row * app.cols + col)

def isEmpty(app, x, y, row, col):
    cellWidth, cellHeight = app.getCellSize
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    if x > cellLeft + cellWidth or y > cellTop + cellHeight:
        return True
    return False
    

def onMousePress(app, mouseX, mouseY):
    if app.menu == True:
        if type(getButton(app, mouseX, mouseY)) == int:
            app.currentLevel = getButton(app, mouseX, mouseY)
    if getButton(app, mouseX, mouseY) == 'start': app.menu = False 
    if getButton(app, mouseX, mouseY) == 'options' and not app.menu: 
        app.options = not app.options
    if app.options == True and getButton(app, mouseX, mouseY) == 'home':
        reset(app)
        app.menu = True
        

def drawMenu(app):
    drawRect(0, 0, app.width, app.height, fill=app.offBlack)
    drawLabel('MENU', app.width//2, app.height*0.1, fill='darkMagenta', 
              size= app.width//10, font='monospace', bold=True, align='center')
    # instructions

    # start button
    drawRect(app.startButtonLeftEdge, app.startButtonTopEdge, app.startButtonWidth,
             app.startButtonHeight, border='darkMagenta', borderWidth = 4, 
             fill=None)
    drawLabel('START', app.startButtonLeftEdge + app.startButtonWidth//2, 
              app.startButtonTopEdge + app.startButtonHeight//2, fill='darkMagenta', 
              size= app.startButtonWidth//5, font='monospace', bold=True, align = 'center')
    drawLevels(app)

def drawLevels(app):
    levelsDrawn = 0
    rows, cols = app.rows, app.cols
    for row in range(rows):
        for col in range(cols):
            if levelsDrawn == app.levels:
                return
            drawCell(app, row, col)
            levelsDrawn += 1
            drawLevelNumber(app, row, col, levelsDrawn)
            

def drawLevelNumber(app, row, col, level):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = app.getCellSize
    cx, cy = cellLeft + cellWidth//2, cellTop + cellHeight//2
    drawLabel(f'{level}', cx, cy, fill='darkMagenta', size = cellWidth//2, 
              font = 'monospace', bold = True, align='center')

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = app.getCellSize
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=None, border= 'darkMagenta',
             borderWidth = 2)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = app.getCellSize
    cellLeft = cellWidth + (2 * cellWidth * col)
    cellTop = app.height * 0.2 + (1.5 * cellHeight * row)
    return (cellLeft, cellTop)

def drawPieces(app):
    previousPiece = (app.groundLeftEdge, app.groundTopEdge, app.groundWidth, app.groundHeight)
    for piece in app.onScreen:
        if piece[1] == 0:
            continue
        else:
            if previousPiece[1] == 0:
                drawRect(piece[0] + previousPiece[2], piece[1], piece[2], piece[3], fill= 'purple')
            else:
                drawRect(piece[0], piece[1], piece[2], piece[3], fill= 'purple')
        previousPiece = piece

def drawGround(app):
    drawRect(app.groundLeftEdge, app.groundTopEdge, app.groundWidth, 
             app.groundHeight, fill='green')

def drawSquare(app):
    x, y = app.squareCenter
    drawRect(x, y, app.squareWidth, app.squareWidth, fill='turquoise', 
             align='center', rotateAngle = app.squareRotation)

def onStep(app):
    takeStep(app)
    bounceSquare(app)

def takeStep(app):
    if app.paused or app.gameOver or app.starting:
        return
    app.count += 1
    if app.count % (app.squareWidth//app.pieceShift) == 0:
        generatePiece(app)
    shiftPieces(app)
    

def generatePiece(app):
    if random.randrange(0,3) == 0:
        emptyGap = randrange(2,5) * app.squareWidth 
        app.onScreen.append((0,0,emptyGap,0))
        return
    if app.onScreen[-1][1] == app.groundTopEdge:
        height = app.bounceHeight - app.squareWidth//2
    else:
        height = random.randrange(1, app.onScreen[-1][3]//app.squareWidth + 2) * app.squareWidth
    width = random.randrange(1,3) * app.squareWidth
    leftEdge = app.width
    topEdge = app.groundTopEdge - height
    app.onScreen.append((leftEdge, topEdge, width, height))


def shiftPieces(app):
    for i in range(1, len(app.onScreen)):
        app.onScreen[i] = (app.onScreen[i][0] - app.pieceShift, app.onScreen[i][1], 
                           app.onScreen[i][2], app.onScreen[i][3])
    checkOnScreen(app)

def checkOnScreen(app):
    count = 0
    while count < len(app.onScreen):
        if app.onScreen[count][0] + app.onScreen[count][2] < 0:
            app.onScreen.pop(count)
        else:
            count += 1

def bounceSquare(app):
    if app.bounceSquareUp == True and app.bounceSquareDown != True:
        squareBouncesUp(app)
    elif app.bounceSquareUp == True and app.bounceSquareDown == True:
        squareBouncesDown(app)
    else:
        squareFalls(app)
        app.bounceSquareUp = False
        app.bounceSquareDown = False
    if makesContact(app): app.gameOver = True

def squareFalls(app):
    if app.squareBottomEdge < impactPoint(app):
        if app.squareRotation < app.startingRotation + 90:
            app.rotatedOnce = True
            app.squareRotation += (app.squareRotatePerStep * 2)
        elif not app.rotatedOnce:
            app.startingRotation = app.squareRotation
        app.squareTopEdge += app.bouncePerStep
        app.squareBottomEdge += app.bouncePerStep
        app.squareCenter = (app.squareCenter[0],
                            app.squareCenter[1] + app.bouncePerStep)
    else:
        app.rotatedOnce = False

def squareBouncesUp(app):
    if app.squareBottomEdge > app.squareBounceStart - (app.bounceHeight):
        app.squareTopEdge -= app.bouncePerStep
        app.squareBottomEdge -= app.bouncePerStep
        if app.squareRotation < (app.startingRotation + 90):
            app.squareRotation += app.squareRotatePerStep
        app.squareCenter = (app.squareCenter[0],
                            app.squareCenter[1] - app.bouncePerStep)
    else:
        app.startingRotation = app.squareRotation
        app.bounceSquareDown = True

def squareBouncesDown(app):
    if app.squareBottomEdge < impactPoint(app):
        app.squareTopEdge += app.bouncePerStep
        # if app.squareRotation < app.startingRotation + 90:
        #     app.squareRotation += (app.squareRotatePerStep * 2)
        app.squareBottomEdge += app.bouncePerStep
        app.squareCenter = (app.squareCenter[0],
                            app.squareCenter[1] + app.bouncePerStep)
    else:
        app.bounceSquareDown = False
        app.bounceSquareUp = False

def makesContact(app):
    squareRightEdge = app.squareLeftEdge + app.squareWidth
    for i in range(len(app.inRangeTopEdge)):
        if (app.groundTopEdge >= app.squareBottomEdge > app.inRangeTopEdge[i] and
            app.inRangeLeftEdge[i] <= squareRightEdge): 
            return True
    return False

def impactPoint(app):
    # return the first impact point within the width of the square
    # each object is in form (leftEdge, topEdge, width, height)
    app.inRangeTopEdge = []
    app.inRangeLeftEdge = []
    for object in app.onScreen:
        if  (object[0] < app.squareLeftEdge + app.squareWidth <= object[0] + object[2] or 
             object[0] <= app.squareLeftEdge < object[0] + object[2]):
            app.inRangeTopEdge.append(object[1])
            app.inRangeLeftEdge.append(object[0])
    return min(app.inRangeTopEdge)

def onKeyPress(app, key):
    if key == 'space' and app.starting == True:
        app.starting = False
    # you can only bounce if you're not current currently bouncing
    if key == 'space'  and app.bounceSquareUp != True and app.bounceSquareDown != True: 
        app.squareBounceStart = app.squareBottomEdge
        app.bounceSquareUp = True
        app.startingRotation = app.squareRotation
    if key == 'p':
        app.paused = not app.paused
    if key == 'r' and app.gameOver: reset(app)

def main():
    runApp(app)
main()



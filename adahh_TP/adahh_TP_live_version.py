from cmu_graphics import *
from types import SimpleNamespace
import random
import time
from adahh_TP_piecesClass import Piece
from adahh_TP_drawing import *
# level clicked on in terms of rows and cols = (row * app.cols) + col

# to fix:
# rotating on falling down and bouncing down, falling down for whenever (falling down fixed)
# ask about lag time with importing an image and how to have multiple lines of 
# text in one drawLabel
# can't jump on game over (fixed)
# victory is near functon, when you win, square goes acroos flat surface until next level starts

# to add:
# - random level generation adjustment (added parameters of levels) for added commplexity
# - different modes (upside down, flying)
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
    app.levels = 1
    app.currentLevel = 1
    app.menu = True
    reset(app)

def reset(app):
    app.flipped = False
    app.starting = True
    # game set-up
    app.stepsPerSecond = 20 + ( 5 * (app.currentLevel // 5))
    app.width = 800
    app.height = 600
    app.count = 0
    app.countsToWin = app.stepsPerSecond * 20 + (app.stepsPerSecond * 5 * app.currentLevel // 5)
    app.pieceShift = 5

    # screen options
    app.paused = False
    app.gameOver = False
    app.options = False
    app.victory = False

    # pop-up dimensions
    app.popUpWidth, app.popUpHeight = app.width//2, app.height//2
    app.popUpLeftEdge, app.popUpTopEdge = app.width*0.25, app.height*0.25
    
    # ground
    app.groundTopEdge = int(app.height * 0.75)
    app.groundHeight= int(app.height*0.25)
    app.groundLeftEdge = 0
    app.groundWidth = app.width

    # square
    square = makeSquare(app)
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
    app.falling = False
    app.squareRotation = 0
    app.squareRotatePerStep = int(90/(app.bounceHeight//app.bouncePerStep))

    # current pieces
    app.pieces = [Piece(app.groundLeftEdge, app.groundTopEdge, app.groundWidth, app.groundHeight)]
    app.portal = False
    # app.portalX, app.portalY, app.portalR = 0, 0, app.squareWidth//2
    app.portalColor = 'indigo'
    app.inRangeTopEdge = [app.pieces[0].top]

    # flipped current pieces
    app.flippedPieces = []


    # menu
    app.offBlack=rgb(52, 46, 55)
    # app.url = 'https://creazilla-store.fra1.digitaloceanspaces.com/icons/3232390/menu-icon-md.png'
    app.startButtonWidth = app.width//5
    app.startButtonHeight = app.height//10
    app.startButtonLeftEdge = app.width//2 - app.startButtonWidth//2
    app.startButtonTopEdge = app.height * 0.8

    app.rows, app.cols = 4, 5
    app.getCellSize = (min(app.width,app.height)//(max(app.rows, app.cols)*2 + 1), min(app.width,app.height)//(max(app.rows, app.cols)*2 + 1))

    #sideMenu
    app.imageWidth, app.imageHeight = 20, 20
    app.sideMenuLines = 3
    app.sideMenuLeftEdge, app.sideMenuTopEdge = app.width//100, app.height//100 + (app.height//50)
    app.sideMenuWidth = app.width//15 - app.width//100
    app.sideMenuHeight = (app.sideMenuLines - 1) * app.height//50
    
    # options
    app.homeButtonWidth = app.popUpWidth//5
    app.homeButtonHeight = app.popUpHeight//10
    app.homeButtonLeftEdge = app.popUpLeftEdge + app.popUpWidth//2 - app.homeButtonWidth//2
    app.homeButtonTopEdge = app.popUpTopEdge + app.popUpHeight * 0.8

    # victory screen    
    app.nextLevelWidth, app.nextLevelHeight = app.popUpWidth//5, app.popUpHeight//10
    app.nextLevelLeftEdge = app.popUpLeftEdge + app.popUpWidth//2 - app.nextLevelWidth//2
    app.nextLevelTopEdge = app.popUpTopEdge + app.popUpHeight * 0.8

    # percentage bar
    app.percentageWidth, app.percentageHeight = app.width*0.8, app.height*0.05
    app.percentageLeftEdge = (app.width-app.percentageWidth) //2
    app.percentageTopEdge = app.height - (app.percentageHeight * 2)

def makeSquare(app):
    square = SimpleNamespace()
    square.width = 40
    square.topEdge = app.groundTopEdge-(square.width)
    square.leftEdge = app.width//2 - square.width//2
    return square

def redrawAll(app):
    if app.menu:
        drawMenu(app)
        return
    drawSideMenu(app)
    drawLabel(f'Current Level: {app.currentLevel}', app.width*0.7, app.height * 0.1, align='left')
    drawGround(app)
    drawSquare(app)
    drawPieces(app)
    if app.portal:
        drawPortal(app, app.portalX, app.portalY, app.portalR, app.portalColor, 7)
    drawPercentage(app)
    if app.gameOver: drawGameOver(app)
    if app.victory: drawVictoryScreen(app)
    if app.starting: drawStartPrompt(app)
    if app.paused: drawPaused(app)
    if app.options: drawOptions(app)

def getButton(app, x, y):
    if (getLevel(app, x, y) != None) and (getLevel(app, x, y) <= app.levels):
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
    if app.victory == True and getButton(app, mouseX, mouseY) == 'home':
        currentLevel = app.currentLevel
        reset(app)
        app.currentLevel = currentLevel + 1
        
def onStep(app):
    takeStep(app)
    bounceSquare(app)

def takeStep(app):
    if app.count == app.countsToWin:
        app.victory = True
        if app.currentLevel == app.levels:
            app.levels += 1
    if app.paused or app.gameOver or app.starting:
        return
    app.count += 1
    if app.count % (app.squareWidth//app.pieceShift) == 0 and app.victory != True:
        generatePiece(app)
    shiftPieces(app)

def generatePiece(app):
    if victoryNear(app):
        return
    # make empty gaps of height ground
    if randrange(0,3) == 0:
        emptyGap = randrange(2,5) * app.squareWidth 
        if app.flipped == True: 
            emptyGap = app.squareWidth
        app.pieces.append(Piece(0,0,emptyGap,0))
        return
    # if previous piece is a gap, next piece height must be app.squareWidth
    if ((app.flipped == True and app.flippedPieces == []) or app.pieces[-1].top == app.groundTopEdge
        or (app.flipped == True and app.flippedPieces[-1].height == 0)):
        height = app.bounceHeight - app.squareWidth//2
    else:
        height = randrange(1, app.pieces[-1].height//app.squareWidth + 2) * app.squareWidth
        if app.flipped:
            height = randrange(1, app.flippedPieces[-1].height//app.squareWidth + 2) * app.squareWidth
    width = randrange(1,3) * app.squareWidth
    leftEdge = app.width
    topEdge = app.groundTopEdge - height
    if app.portal == False and app.count > app.countsToWin//3:
        app.portal = True
        app.portalR = app.squareWidth//2
        app.portalX= leftEdge + width//2
        app.portalY = topEdge + app.squareWidth//2 if app.flipped else topEdge-app.squareWidth//2
    if app.flipped == True:
        topEdge = 0
        app.flippedPieces.append(Piece(leftEdge, topEdge, width, height))
        return
    app.pieces.append(Piece(leftEdge, topEdge, width, height))

def victoryNear(app):
    countsRemaining = app.countsToWin-app.count
    shiftsRemaining = app.width - (app.squareLeftEdge+app.squareWidth)
    shiftsRemaining = shiftsRemaining/app.pieceShift
    if countsRemaining < (shiftsRemaining + (app.squareWidth//app.pieceShift)*3):
        return True
    return False

def shiftPieces(app):
    piecesToMove = app.pieces
    if app.flipped:
        piecesToMove = app.flippedPieces
    for piece in piecesToMove:
        if piece.top == app.groundTopEdge:
            continue
        piece.shift(app.pieceShift)
    if app.portal:
        app.portalX -= app.pieceShift
    if app.portal == True and app.portalX <= app.squareLeftEdge + app.squareWidth//2:
        app.portal = False
        app.pieces = app.pieces[:1]
        print(app.pieces)
        # app.flippedPieces = []
        app.flipped = not app.flipped
    checkOnScreen(app)

def checkOnScreen(app):
    if app.portal == True:
        if app.portalX + app.portalR*2 < 0:
            app.portal = False
    piecesToMove = app.pieces
    if app.flipped:
        piecesToMove = app.flippedPieces
    count = 0
    while count < len(piecesToMove):
        if piecesToMove[count].left + piecesToMove[count].width < 0:
            if app.flipped:
                app.flippedPieces.pop(count)
            else:
                app.pieces.pop(count)
        else:
            count += 1

def bounceSquare(app):
    if app.paused or app.gameOver or app.victory: return
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
    app.falling = True
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
        app.falling = False
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
    for piece in app.pieces:
        if  (piece.left < app.squareLeftEdge + app.squareWidth <= piece.left + piece.width or 
             piece.left <= app.squareLeftEdge < piece.left + piece.width):
            app.inRangeTopEdge.append(piece.top)
            app.inRangeLeftEdge.append(piece.left)
    return min(app.inRangeTopEdge)

def onKeyPress(app, key):
    if key == 'space' and app.starting == True:
        app.starting = False
    # you can only bounce if you're not currently bouncing
    if key == 'space'  and app.bounceSquareUp != True and app.bounceSquareDown != True and app.falling != True: 
        app.squareBounceStart = app.squareBottomEdge
        app.bounceSquareUp = True
        app.startingRotation = app.squareRotation
    if key == 'p':
        app.paused = not app.paused
    if key == 'r' and app.gameOver: reset(app)

def main():
    runApp(app)
main()



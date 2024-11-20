# base draw set up
from cmu_graphics import *

def drawPercentage(app):
    drawRect(app.percentageLeftEdge, app.percentageTopEdge, app.percentageWidth, app.percentageHeight,
             border='black', borderWidth=4, fill='white')
    if app.count > 0 and app.victory != True:
        percentage = app.count/app.countsToWin
        width = app.percentageWidth * percentage
        drawRect(app.percentageLeftEdge, app.percentageTopEdge, width, 
                 app.percentageHeight, fill='limeGreen', border='black')
        drawLabel(f'{int(percentage * 100)}%', app.percentageLeftEdge + width, 
                  app.percentageTopEdge + app.percentageHeight//2,align='center')
        
def drawGameOver(app):
    drawRect(app.popUpLeftEdge, app.popUpTopEdge, app.popUpWidth, app.popUpHeight,
             fill = app.offBlack, border='black', borderWidth = 4)
    drawLabel("GAME OVER", app.width//2, app.popUpTopEdge + app.popUpHeight * 0.1,
              size = app.width*0.5//10, font='monospace', bold=True, fill='darkMagenta')
    drawLabel("press 'r' to try again", app.width//2, app.popUpTopEdge + app.popUpHeight * 0.2,
              size = app.width*0.2//10, font='monospace', bold=True, fill='darkMagenta')
    drawLabel(f'{int((app.count/app.countsToWin)*100)}%complete', app.width//2, 
              app.popUpTopEdge + app.popUpHeight * 0.3, size = app.width*0.2//10, 
              font='monospace', bold=True, fill='darkMagenta' )
    
def drawVictoryScreen(app):
    drawRect(app.popUpLeftEdge, app.popUpTopEdge, app.popUpWidth, app.popUpHeight,
             fill=None, border='black', borderWidth = 4)
    drawLabel("LEVEL COMPLETE", app.width//2, app.popUpTopEdge + app.popUpHeight * 0.1,
              size = app.width*0.5//10, font='monospace', bold=True, fill='darkMagenta')
    drawRect(app.nextLevelLeftEdge, app.nextLevelTopEdge, app.nextLevelWidth, app.nextLevelHeight,
             border='darkMagenta', borderWidth=4, fill=None)
    drawLabel('NEXT', app.nextLevelLeftEdge + app.nextLevelWidth//2, 
              app.nextLevelTopEdge + app.nextLevelHeight//2, fill='darkMagenta', 
              size= app.nextLevelWidth//5, font='monospace', bold=True, align= 'center')
    
def drawPaused(app):
    drawRect(app.popUpLeftEdge, app.popUpTopEdge, app.popUpWidth, app.popUpHeight, 
             fill=app.offBlack, border = 'black', borderWidth = 4)
    drawLabel('PAUSED', app.width//2, app.popUpTopEdge + app.popUpHeight*0.1, 
              size= app.width*0.5//10, font='monospace', bold=True, fill='darkMagenta', 
              align='center')
    # add how to resume, current level progress, restart button
    

def drawStartPrompt(app):
    cx = app.width//2
    cy = app.groundHeight
    drawLabel("press 'space' to begin...", cx, cy, fill='black', font='monospace',
              bold=True, size=app.width//20)

def drawOptions(app):
    drawRect(app.popUpLeftEdge, app.popUpTopEdge, app.popUpWidth, app.popUpHeight, 
             fill=app.offBlack, border = 'black', borderWidth = 4)
    drawLabel('OPTIONS', app.width//2, app.popUpTopEdge + app.popUpHeight*0.1, 
              size= app.width*0.5//10, font='monospace', bold=True, fill='darkMagenta', 
              align='center')
    #return to homescreen/menu
    drawRect(app.homeButtonLeftEdge, app.homeButtonTopEdge, app.homeButtonWidth,
             app.homeButtonHeight, border='darkMagenta', borderWidth = 4, 
             fill=None)
    drawLabel('HOME', app.homeButtonLeftEdge + app.homeButtonWidth//2, 
              app.homeButtonTopEdge + app.homeButtonHeight//2, fill='darkMagenta', 
              size= app.homeButtonWidth//5, font='monospace', bold=True, align= 'center')

def drawSideMenu(app):
    for i in range (1,app.sideMenuLines + 1):
        x0, y0 = app.width//100, app.height//100 + (i*app.height//50)
        x1, y1 = app.width//15, app.height//100 + (i*app.height//50)
        drawLine(x0, y0, x1, y1)

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
    if app.flipped:
        for piece in app.flippedPieces:
            if piece.height == 0:
                continue
            if app.flippedPieces != []:
                previousPiece = app.flippedPieces[-1]
            else:
                previousPiece = None
            if previousPiece != None:
                if previousPiece.height == 0:
                    drawRect(piece.left + previousPiece.width, piece.top, piece.width, piece.height, fill= 'purple')
                else:
                    drawRect(piece.left, piece.top, piece.width, piece.height, fill= 'purple')
                previousPiece = piece

    else:
        for piece in app.pieces:
            if piece.height == 0:
                continue
            else:
                if previousPiece[3] == 0:
                    drawRect(piece.left + previousPiece.width, piece.top, piece.width, piece.height, fill= 'purple')
                else:
                    drawRect(piece.left, piece.top, piece.width, piece.height, fill= 'purple')
            previousPiece = (piece.left, piece.top, piece.width, piece.height)

def drawPortal(app,x, y, r, color, borderWeight):
    if r < 2:
        drawCircle(x, y, r, border=color, borderWidth = borderWeight, fill= color)
    else:
        drawCircle(x, y, r, border=color, borderWidth = borderWeight, fill= None)
        if color == 'indigo':
            return drawPortal(app, x, y, r*0.85, 'deepPink', borderWeight*0.85)
        else:
            return drawPortal(app, x, y, r*0.85, 'indigo', borderWeight*0.85)
def drawGround(app):
    drawRect(app.groundLeftEdge, app.groundTopEdge, app.groundWidth, 
             app.groundHeight, fill='green')

def drawSquare(app):
    x, y = app.squareCenter
    drawRect(x, y, app.squareWidth, app.squareWidth, fill='turquoise', 
             align='center', rotateAngle = app.squareRotation)
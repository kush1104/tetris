from tkinter import *
import random
import copy

# MODEL VIEW CONTROLLER (MVC)
####################################
# MODEL:       the data
# VIEW:        redrawAll and its helper functions
# CONTROLLER:  event-handling functions and their helper functions
####################################

def init(data):
    # board data
    data.emptyColor = 'blue'
    data.rows = 15
    data.cols = 10
    margin = 2
    padding = 2
    data.cellSize = data.height/(data.rows + padding*margin)
    data.leftMargin = (data.width - (data.cellSize * data.cols))/2
    data.topMargin = data.cellSize
    initBoard(data)
    
    #basic piece and game data
    data.isGameOver = False
    data.isPaused = False
    data.score = 0
    data.tetrisPieces = makePieces()
    #cite: from course notes
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
                         "cyan", "green", "orange" ]
    
    newFallingPiece(data)
    
def initBoard(data):
    data.board = []
    #2d list, size: row x col, all cells are data.emptyColor
    for row in range(data.rows):
        rowList = []
        for col in range(data.cols):
            rowList.append(data.emptyColor)
        data.board.append(rowList)
        
def makePieces():
    #Seven "standard" pieces (tetrominoes)
    #Cite: from course notes
  iPiece = [[ True,  True,  True,  True]]
  
  jPiece = [[ True, False, False ],[ True, True,  True]]
  
  lPiece = [[ False, False, True],[ True,  True,  True]]
  
  oPiece = [[ True, True],[ True, True]]
  
  sPiece = [[ False, True, True],[ True,  True, False ]]
  
  tPiece = [[ False, True, False ],[ True,  True, True]]

  zPiece = [[ True,  True, False ],[ False, True, True]]
  
  tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
  return tetrisPieces

def newFallingPiece(data):
    #randomly select piece and color and start at the top middle
    data.fallingPiece  = random.choice(data.tetrisPieces)
    data.fallingPieceColor = random.choice(data.tetrisPieceColors)
    data.fallingPieceRows = len(data.fallingPiece)
    data.fallingPieceColumns = len(data.fallingPiece[0])
    
    data.fallingPieceRow = 0
    data.fallingPieceCol = (data.cols//2) - (data.fallingPieceColumns//2)

def moveFallingPiece(data, drow, dcol):
    #move in direction
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if not fallingPieceIsLegal(data): #if illegal, move back 
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True
        
def rotateFallingPiece(data):
    #stored piece, location, and dimensions in local variables
    oldFallingPiece = copy.deepcopy(data.fallingPiece)
    oldRow = data.fallingPieceRow
    oldCol = data.fallingPieceCol
    oldRows = data.fallingPieceRows
    oldCols = data.fallingPieceColumns
    
    #calculate new row coordinate
    newCenter = oldRow + oldRows//2
    newRows = oldCols
    newRow = (newCenter - newRows//2)
    data.fallingPieceRow = newRow
    
    #calculate new col coordinate
    newCenter = oldCol + oldCols//2
    newCols = oldRows
    newCol = (newCenter - newCols//2)
    data.fallingPieceCol = newCol    
    
    #rotate piece
    ccwPieceRotation(data)
    
    #if illegal, change it back
    if not fallingPieceIsLegal(data):
        data.fallingPiece = oldFallingPiece
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol
        data.fallingPieceRows = oldRows
        data.fallingPieceColumns = oldCols
        
def ccwPieceRotation(data): 
    #counter-clockwise rotation of falling piece
    newPiece = []
    for col in range(len(data.fallingPiece[0])-1, -1, -1):
        newRowList = []
        for row in range(len(data.fallingPiece)):
            newRowList.append(data.fallingPiece[row][col])
        newPiece.append(newRowList)
    
    data.fallingPiece = newPiece
    data.fallingPieceRows = len(data.fallingPiece)
    data.fallingPieceColumns = len(data.fallingPiece[0])
    
def fallingPieceIsLegal(data):
    #checks if location of piece is on board and not on top of other piece
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                if (data.fallingPieceRow + row < 0 
                or data.fallingPieceRow + row >= data.rows
                or data.fallingPieceCol + col < 0 
                or data.fallingPieceCol + col >= data.cols
                or data.board[data.fallingPieceRow+row]
                [data.fallingPieceCol+col]
                != data.emptyColor):
                    return False
    return True

def placeFallingPiece(data):
    #places piece on to board
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                data.board[data.fallingPieceRow+row]\
                [data.fallingPieceCol+col] = data.fallingPieceColor
                
def removeFullRows(data):
    breakAndContinue = False
    newRow = len(data.board)
    fullRows = 0
    for oldRow in range(len(data.board)-1, -1, -1): 
        for col in range(len(data.board[oldRow])):
            #checks if there is any empty space in row
            if data.board[oldRow][col] == data.emptyColor:
                newRow -= 1
                data.board[newRow] = copy.copy(data.board[oldRow])
                breakAndContinue= True #no need to check more columns of row
                break
        if breakAndContinue:
            breakAndContinue = False
            continue
        fullRows += 1
    
    data.score += (fullRows ** 2)

# These are the CONTROLLERs.
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # control piece movement
    if event.keysym == 'Left':
        moveFallingPiece(data, 0, -1)
    elif event.keysym == 'Right':
        moveFallingPiece(data, 0, 1)
    elif event.keysym == 'Up':
        rotateFallingPiece(data)
    elif event.keysym == 'Down':
        moveFallingPiece(data, 1, 0)
    elif event.keysym == 'space':
        while moveFallingPiece(data,1,0): continue 
        placeFallingPiece(data)
    #restart game
    elif event.keysym == 'r':
        init(data)
    #pause game
    elif event.keysym == 'p':
        data.isPaused = not data.isPaused

def timerFired(data):
    if data.isPaused:
        return
    
    if moveFallingPiece(data, 1, 0) == False: #moves piece down until it can't
        placeFallingPiece(data)
        newFallingPiece(data)
        removeFullRows(data)
        if not fallingPieceIsLegal(data):
            data.isGameOver = True
    
# This is the VIEW
def redrawAll(canvas, data):
    if data.isGameOver:
        #Game Over Screen
        canvas.create_text(data.width/2, data.height/5, text='Game Over!')
        canvas.create_text(data.width/2, 3*data.height/5, 
                           text='Press "r" to restart.')
        return
    drawGame(canvas, data)
    drawScore(canvas, data)
    
def drawGame(canvas, data):
    #background screen
    canvas.create_rectangle(0, 0, data.width, data.height, fill = 'orange')
    #informational text
    canvas.create_text(data.width/2, 3*data.topMargin/2,
                       text = 'Press "p" to pause')
    canvas.create_text(data.width/2, data.height - data.topMargin, 
                       text = 'Press "r" to restart')
    
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)

def drawBoard(canvas, data):
    #iterates through every cell and draws
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])

def drawScore(canvas, data):
    #displays score for user
    canvas.create_text(data.width/2, data.topMargin/2, 
                       text = ('Score: ' + str(data.score)))

def drawFallingPiece(canvas, data):
    #iterates through every cell of falling piece and draws
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                drawCell(canvas, data, 
                         row+data.fallingPieceRow, col+data.fallingPieceCol, 
                         data.fallingPieceColor)

def drawCell(canvas, data, row, col, color):
    padding = 2 #allows more of a margin on top and bottom for space for text
    
    #get coordinates of cell
    x0 = data.leftMargin + (col*data.cellSize)
    y0 = padding*data.topMargin +(row*data.cellSize)
    x1 = data.leftMargin + ((col+1)*data.cellSize)
    y1 = padding*data.topMargin + ((row+1)*data.cellSize)
    
    #create outer black border
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'black')
    
    #create inner cell
    data.border = data.cellSize/10
    canvas.create_rectangle(x0+data.border, y0+data.border, 
                            x1-data.border, y1-data.border,
                            fill = color)

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(300, 475)

__author__ = 'Charlie'
from tkinter import *
import re

player1RemovedPiecesList = []
player2RemovedPiecesList = []
coordsDict = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}

def run():
    root = Tk()
    theboard = Game(root)
    root.mainloop()


class Game:
    def __init__(self,root):

        self.root = root

        self.board = Canvas(self.root,
                            width = 500,
                            height = 500)
        self.board.pack()
        self.board.bind("<Button-1>", self.clicked)
        self.player1name = 'steve'
        self.player2name = 'john'
        self.player1color = 'red'
        self.player2color = 'blue'
        self.selectedPieceName = None

        self.createboard('white','black')



    def __repr__(self):
        return 'The Game Board'

    def __str__(self):
        return print('The Game Board')

    def createboard(self, colora, colorb):
        '''Draws a checker board in two given colors and will create a 2D list to store data about
        the board in.'''
        global coordsDict
        # (xstart,ystart, xend, yend)
        row = 0
        color = colora
        self.boardlist =[]
        while row < 8:
            col = 0

            if color == colora:
                color = colorb
            elif color == colorb:
                color = colora

            rowlist = []
            while col < 8:

                if color == colora:
                    color = colorb
                elif color == colorb:
                    color = colora


                # Cords(Left, top, right, bottom)
                self.board.create_rectangle(row*50, col*50 + 100, row*50 + 50, col*50 + 150, fill = color)
                rowlist.append([color, 'empty', (coordsDict[col], 8-row), row, col])
                #print(rowlist)

                    # empty signifies the space is unoccupied
                    # The tuple in position 3 is the "Chess coordinates"
                col += 1
            row+=1
            self.boardlist.append(rowlist)


        # The following will create all the piece and name each piece PlayerName# where #
        # corresponds to an iterator that will be different for each piece of a specific player
        # The piece names and their color are then inserted into the apropriate board
        # tiles changing the format of a tile that is occupied to ['tile color', ['piece color', 'piece name']]
    
        rownum = 0
        count = 1
        for row in self.boardlist:
            colnum = 0
            if rownum <3:
                for tile in row:
                    if tile[0] == colora:
                        piecename = self.player1name+str(count)
                        exec(piecename+' = Piece(rownum,colnum,self.player1color,piecename,self, "reg")')
                        self.boardlist[rownum][colnum][1] = [self.player1color,piecename, "reg"]

                        count += 1
                    colnum += 1
            rownum +=1

        rownum = 0
        count = 1
        for row in self.boardlist:
            colnum = 0
            if rownum <8 and rownum >4:
                for tile in row:
                    if tile[0] == colora:
                        piecename = self.player2name+str(count)

                        exec(piecename+' = Piece(rownum,colnum,self.player2color,piecename,self, "reg")')
                        self.boardlist[rownum][colnum][1] = [self.player2color,piecename,"reg"]
                        count += 1
                    colnum += 1
            rownum +=1


    def clicked(self,event):
        '''determines if an empty square has been selected or a piece and then returns something useful'''
        try:
            a = self.pieceSelectedName
        except:
            self.pieceSelectedName = None

        # Get the location of the click
        x = self.board.canvasx(event.x)
        y = self.board.canvasy(event.y)
        row = int((y-100) // 50)
        col = int(x // 50)
        tile = self.boardlist[row][col] #The chosen tile on the board
        validMove = False #at least until shown to be true

        if tile[1] != 'empty': #If there is a piece in the tile
            self.pieceOldRow = row
            self.pieceOldCol = col
            self.pieceSelectedName = tile[1][1] # get the name of the piece that was selected
            self.pieceSelectedColor = tile[1][0]
            self.startingLocation = (tile[3],tile[4]) # gets the row and collumn that the piece starts in


        elif tile[1] == 'empty' and self.pieceSelectedName != None: #The tile chosen is empty and the user has
                                                                    #already selected a piece
            #Get the relative movements of the piece
            relRow = self.startingLocation[0]-row
            relCol = self.startingLocation[1]-col

            if relRow == 0 or relCol == 0: #then you are moving straight forwards or backwards
                validMove = False

            # The conditions where you are trying to make a normal move
            elif self.startingLocation[0] == row-1 and self.pieceSelectedColor == self.player1color:
                validMove = True

            elif self.startingLocation[0] == row+1 and self.pieceSelectedColor == self.player2color:
                validMove = True

            elif self.startingLocation[0] == row+1 or self.startingLocation[0] == row-1 \
                    and self.boardlist[self.pieceOldRow][self.pieceOldCol][1][2] == 'king':
                validMove = True

            # The conditions where you are trying to make a jump
            elif self.startingLocation[0] == row-2 and self.pieceSelectedColor == self.player1color:

                if self.startingLocation[1] == col-2 and self.boardlist[row-1][col-1][1][0] == self.player2color:
                    validMove = True
                    shouldIRecurse = True
                    self.removePiece(row-1,col-1)

                if self.startingLocation[1] == col+2 and self.boardlist[row-1][col+1][1][0] == self.player2color:
                    validMove = True
                    shouldIRecurse = True
                    self.removePiece(row-1,col+1)

            elif self.startingLocation[0] == row+2 and self.pieceSelectedColor == self.player2color:

                if self.startingLocation[1] == col-2 and self.boardlist[row+1][col-1][1][0] == self.player1color:
                    validMove = True
                    shouldIRecurse = True
                    self.removePiece(row+1,col-1)

                if self.startingLocation[1] == col+2 and self.boardlist[row+1][col+1][1][0] == self.player1color:
                    validMove = True
                    shouldIRecurse = True
                    self.removePiece(row+1,col+1)

            # If you are a king trying to make a jump
            elif self.boardlist[self.pieceOldRow][self.pieceOldCol][1][2] == 'king' and\
                (self.startingLocation[0] == row+2 or self.startingLocation[0] == row-2):
                validMove = True
                shouldIRecurse = True
                if self.pieceSelectedColor == self.player1color:
                    pass


            else:
                print("You did not select a valid move")

        else:
            print("Error: The selection and/or order was invalid")

        if validMove == True:
            #Update the GUI and the list
            self.boardlist[self.pieceOldRow][self.pieceOldCol][1] = 'empty' #reset old tile to empty
            self.boardlist[row][col][1] = [self.pieceSelectedColor, self.pieceSelectedName] #update new tile
            self.board.move(self.pieceSelectedName, -50*(relCol), -50*(relRow)) #move the piece in the GUI

            # Where you can legally move:
                # A Spot diagonally in front of your piece that is unoccupied
                # A Spot diagonaly behind your piece that is unoccupied if your piece is a king
                # A Spot diagonally infront (behind too if your piece is a king)
                    # of your piece 2 that is unoccupied if there is a piece
                    # in between the spot where you are and the unoccupied spot
                    # This needs some kind of recursive check

    def removePiece(self, row, col):
        global player1RemovedPiecesList, player2RemovedPiecesList
        removedPiece = self.boardlist[row][col][1][1]

        self.board.delete(removedPiece)
        self.boardlist[row][col][1] = 'empty'
        playerName = re.findall('[A-Za-z ]+', removedPiece)
        playerName = str(playerName[0])

        if playerName == self.player1name:
            color = self.player1color
            player1RemovedPiecesList.append(removedPiece)
            self.board.create_oval(405,100+10*len(player1RemovedPiecesList),445,
                                   140+10*len(player1RemovedPiecesList),
                                   fill = self.player1color)
        else:
            color = self.player2color
            player2RemovedPiecesList.append(removedPiece)
            self.board.create_oval(455,100+10*len(player2RemovedPiecesList),495,
                                   140+10*len(player2RemovedPiecesList),
                                   fill = self.player2color)




class Piece:
    def __init__(self, row, col, color, name, theboard, type):
        '''Createas a playing piece at the given row and column (Note: row and column indices start at 0'''
        self.loc = theboard.board.create_oval(col*50 + 5, row*50 +105, col*50 + 45, row*50 + 145,
                                              fill = color,
                                              tags = name)
        self.color = color
        self.theboard = theboard
        self.name = name
        self.type = type

    def move(self, row, col):
        self.loc = self.theboard.board.create_oval(col*50 + 5, row*50 +105, col*50 + 45, row*50 + 145,
                                              fill = 'green')
        #test = self.theboard.board.create_oval(200,200,300,300, fill = "green")

    def kingIt(self):
        self.type = "king"

run()
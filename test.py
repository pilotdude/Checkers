__author__ = 'Charlie'
from tkinter import *
# The first entries in boardlist look like this:
firstTwo = [[['white', ['red', 'steve1', 'reg'], ('a', 8), 0, 0], ['black', 'empty', ('b', 8), 0, 1]]]
beastlist = []
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

                        exec(piecename+' = Piece(rownum,colnum,self.player1color,piecename,self)')
                        self.boardlist[rownum][colnum][1] = [self.player1color,piecename]

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

                        exec(piecename+' = Piece(rownum,colnum,self.player2color,piecename,self)')
                        self.boardlist[rownum][colnum][1] = [self.player2color,piecename]
                        count += 1
                    colnum += 1
            rownum +=1





    def clicked(self,event):
        '''determines if an empty square has been selected or a piece and then returns something useful'''

        x = self.board.canvasx(event.x)
        y = self.board.canvasy(event.y)

        row = int((y-100) // 50)
        col = int(x // 50)
        tile = self.boardlist[row][col]
        tilecolor = tile[0]
        tileIndicator = tile[1]
        print(tile)
        if tileIndicator != "empty": #the spot has a piece in it
            self.pieceSelected = True
            print(tile)
            # Get that piece's name
            self.selectedPieceName = tile[1][1]
            self.selectedPieceColor = tile[1][0]
            print(self.selectedPieceName)
            return self.pieceSelected


        if self.selectedPieceName != None and self.pieceSelected == True:
            exec(self.selectedPieceName+'.move(1,1)')
            if self.board.find_withtag(CURRENT):
                self.board.itemconfig(CURRENT, fill='red')
                self.board.update_idletasks()
                self.board.after(200)
                self.board.itemconfig(CURRENT, fill = tilecolor)

                # Now move the piece to this spot
                #print(self.selectedPieceName+'.move(1,1)')
                #print(beastlist)

                self.selectedPieceName = None

        elif tileIndicator == "empty": # the spot does not have a piece in it
            self.pieceSelected = False

            

class Piece:
    def __init__(self, row, col, color, name, theboard):
        '''Createas a playing piece at the given row and column (Note: row and column indices start at 0'''
        self.loc = theboard.board.create_oval(col*50 + 5, row*50 +105, col*50 + 45, row*50 + 145,
                                              fill = color)
        self.color = color
        self.theboard = theboard
        self.name = name
        #self.row = row
        #self.col = col

        global beastlist
        beastlist.append(self.name)



    def move(self, row, col):
        self.loc.cords()
        #test = self.theboard.board.create_oval(200,200,300,300, fill = "green")

run()
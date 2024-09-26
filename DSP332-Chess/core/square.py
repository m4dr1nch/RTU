import tkinter as tk
from PIL import Image, ImageTk

from utils.colors import Colors

class Square(object):
    def __init__(self, board, ui_row, chess_row, column):
        self.board = board
        self.piece = None
        self.attacker = None

        self.ui_row = ui_row
        self.ui_col = column
        self.row = chess_row
        self.col = column

        if (self.ui_row + self.ui_col) % 2 == 0: self.color = Colors.LIGHT_VIOLET
        else: self.color = Colors.DARK_VIOLET
        
        # Create a label with an empty image
        # Needed for constant label size
        self.TK_Label = tk.Label(board.TK_Canvas, bd=0, bg=self.color, image=board.TK_Null_Image, height=100, width=100)
        self.TK_Label.image = board.TK_Null_Image
        self.TK_Label.grid(row=self.ui_row, column=self.ui_col)



    def getChord(self):
        return (self.col, self.row)



    def setIcon(self, tk_icon):
        self.TK_Label.configure(image=tk_icon)
        self.TK_Label.image = tk_icon



    def unsetIcon(self):
        self.TK_Label.configure(image=self.board.TK_Null_Image)
        self.TK_Label.image = self.board.TK_Null_Image



    def setPiece(self, piece):
        piece.square = self
        self.board.game.game_state[self.col][self.row] = piece.id
        self.piece = piece
        self.attacker = None
        self.setIcon(piece.TK_Icon)



    def unsetPiece(self):
        self.board.game.game_state[self.col][self.row] = 0
        self.piece = None
        self.attacker = None
        self.unsetIcon()



    def selectSquare(self):
        # We loop over the squares that the current squares piece is moves
        for (row, col) in self.piece.moves:

            square = self.board.getSquare(row, col)

            # We set the dot icon if there is no piece on the square
            if square.piece is None:
                square.setIcon(self.board.TK_Dot_Image)
            else:
                # If the square contains a piece then we create a new image
                # We create a composite ImageTk from  piece and dot icons
                icon_dot = self.board.dot_image.copy()
                icon_piece = square.piece.icon.copy()
                icon_piece.paste(icon_dot, (0, 0), icon_dot)
                square.setIcon(ImageTk.PhotoImage(icon_piece))

            # We also set the square as attacked
            square.attacker = self

        # We also set the selected square as the clicked square
        self.board.s_selected = self



    def unselectSquare(self):
        # We loop over the squares that the selected square is moves
        for (col, row) in self.piece.moves:
            square = self.board.getSquare(col, row)

            # We then unset the squares icon and mark it as not attacked
            if square.piece is None: square.unsetIcon()
            else: square.setIcon(square.piece.TK_Icon)

            square.attacker = None

        # We also set the selected square to none
        self.board.s_selected = None

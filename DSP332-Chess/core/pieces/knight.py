import tkinter as tk
from PIL import ImageTk
from core.pieces import Piece

class Knight(Piece):
    def __init__(self, field, color):
        Piece.__init__(self, field, color)

        self.type = 'Knight'
        if self.color == 'white': self.id = 4
        else: self.id = 3
        self.setIcon()



    def genMoves(self, board_state):
        col = self.square.col
        row = self.square.row

        for i in range(-2, 3):
            if abs(i) == 2:
                target_col = col + i
                
                target_row_min = row - 1
                target_row_max = row + 1

                if Piece.inRange(target_col, target_row_min):
                    if self.inTeam(board_state, target_col, target_row_min):
                        self.addProtected(target_col, target_row_min)
                    else:
                        self.moves.add((target_col, target_row_min))
                
                if Piece.inRange(target_col, target_row_max):
                    if self.inTeam(board_state, target_col, target_row_max):
                        self.addProtected(target_col, target_row_max)
                    else:
                        self.moves.add((target_col, target_row_max))
            
            if abs(i) == 1:
                target_col = col + i

                target_row_min = row - 2
                target_row_max = row + 2

                if Piece.inRange(target_col, target_row_min):
                    if self.inTeam(board_state, target_col, target_row_min):
                        self.addProtected(target_col, target_row_min)
                    else:
                        self.moves.add((target_col, target_row_min))
                
                if Piece.inRange(target_col, target_row_max):
                    if self.inTeam(board_state, target_col, target_row_max):
                        self.addProtected(target_col, target_row_max)
                    else:
                        self.moves.add((target_col, target_row_max))

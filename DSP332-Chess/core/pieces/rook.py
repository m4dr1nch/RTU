import tkinter as tk
from PIL import ImageTk
from core.pieces import Piece

class Rook(Piece):
    def __init__(self, field, color):
        Piece.__init__(self, field, color)

        self.type = 'Rook'
        self.has_moved = False
        if self.color == 'white': self.id = 8
        else: self.id = 8
        self.setIcon()



    def genMoves(self, board_state):
        # Enumerate north/south
        self.enumerate(0, 1, board_state)
        self.enumerate(0, -1, board_state)
        
        # Enumerate west/east
        self.enumerate(1, 0, board_state)
        self.enumerate(-1, 0, board_state)

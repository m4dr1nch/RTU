import tkinter as tk
from PIL import ImageTk
from core.pieces import Piece

class Bishop(Piece):
    def __init__(self, field, color):
        Piece.__init__(self, field, color)
        
        self.type = 'Bishop'
        if self.color == 'white': self.id = 6
        else: self.id = 5
        self.setIcon()



    def genMoves(self, board_state):
        # Enumerate north-east/south-west
        self.enumerate(1, 1, board_state)
        self.enumerate(-1, -1, board_state)

        # Enumerate north-west/south-west
        self.enumerate(1, -1, board_state)
        self.enumerate(-1, 1, board_state)

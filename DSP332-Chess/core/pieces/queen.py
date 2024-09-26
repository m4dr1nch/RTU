import tkinter as tk
from PIL import ImageTk
from core.pieces import Piece

class Queen(Piece):
    def __init__(self, field, color):
        Piece.__init__(self, field, color)

        self.type = 'Queen'
        if self.color == 'white': self.id = 10
        else: self.id = 9
        self.setIcon()



    def genMoves(self, board_state):
        # Enumerate north/south
        self.enumerate(0, 1, board_state)
        self.enumerate(0, -1, board_state)
        
        # Enumerate west/east
        self.enumerate(1, 0, board_state)
        self.enumerate(-1, 0, board_state)
        
        # Enumerate north-east/south-west
        self.enumerate(1, 1, board_state)
        self.enumerate(-1, -1, board_state)

        # Enumerate north-west/south-west
        self.enumerate(1, -1, board_state)
        self.enumerate(-1, 1, board_state)

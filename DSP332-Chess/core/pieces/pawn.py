import tkinter as tk
from PIL import ImageTk
from core.pieces import Piece

class Pawn(Piece):
    def __init__(self, field, color):
        Piece.__init__(self, field, color)

        self.type = 'Pawn'
        self.inline_moves = set()
        self.has_moved = False
        self.is_frenchable = False
        self.is_french = False
        if self.color == 'white': self.id = 2
        else: self.id = 1
        self.setIcon()



    def genMoves(self, board_state):
        col = self.square.col
        row = self.square.row

        self.inline_moves.clear()

        if self.color == 'white':
            prefix = 1
        else:
            prefix = -1

        for i in range(-1, 2):
            target_col = col + i
            target_row = row + prefix

            if not Piece.inRange(target_col, target_row): continue

            if i != 0:
                if board_state[target_col][target_row] != 0:
                    if self.inTeam(board_state, target_col, target_row):
                        self.addProtected(target_col, target_row)
                    else:
                        self.moves.add((target_col, target_row))
                else:
                    self.addProtected(target_col, target_row)
            else:
                if board_state[target_col][target_row] == 0:
                    self.addInline((target_col, target_row))

                    if not self.has_moved:
                        if board_state[target_col][target_row + prefix] == 0:
                            self.addInline((target_col, target_row + prefix))


        self.addFrench(board_state, self.color)



    def addFrench(self, board_state, color):
        pos = self.getChord()
        self.is_french = False

        if color == 'white':
            if pos[1] != 4: return
            prefix = 1
            target = 1
        elif color == 'black':
            if pos[1] != 3: return
            prefix = -1
            target = 2
        else: raise Exception("Incorrect color specification")

        if board_state[pos[0]-1][pos[1]] == target:
            if self.square.board.getPiece(pos[0] - 1, pos[1]).is_frenchable:
                self.moves.add((pos[0]-1, pos[1]+prefix))
                self.is_french = True


        if board_state[pos[0]+1][pos[1]] == target:
            if self.square.board.getPiece(pos[0]+1, pos[1]).is_frenchable:
                self.moves.add((pos[0]+1, pos[1]+prefix))
                self.is_french = True



    def addInline(self, move):
        self.inline_moves.add(move)

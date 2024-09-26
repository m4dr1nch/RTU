import tkinter as tk
from PIL import ImageTk
from core.pieces import Piece

class King(Piece):
    def __init__(self, square, color):
        Piece.__init__(self, square, color)

        self.type = 'King'
        self.has_moved = False
        self.in_check = False
        if self.color == 'white': self.id = 12
        else: self.id = 11
        self.setIcon()



    def genMoves(self, board_state):
        col = self.square.col
        row = self.square.row

        for c in range(-1, 2):
            for r in range(-1, 2):
                target_col = col + c
                target_row = row + r

                if Piece.inRange(target_col, target_row):
                    if board_state[target_col][target_row] == 0:
                        self.moves.add((target_col, target_row))
                    elif not self.inTeam(board_state, target_col, target_row):
                        self.moves.add((target_col, target_row))
                    else:
                        self.addProtected(target_col, target_row)
        
        if self.has_moved == False:
            self.addCastles(board_state, self.color)



    def addCastles(self, board_state, color):
        if color == 'white':
            l_rook = (0, 0)
            r_rook = (7, 0)
            i_rook = 8
            o_moves = self.square.board.game.bl_attacking
        elif color == 'black':
            l_rook = (0, 7)
            r_rook = (7, 7)
            i_rook = 7
            o_moves = self.square.board.game.wh_attacking
        else: raise Exception("Incorrect color specification")
        
        king_pos = self.getChord()

        if board_state[l_rook[0]][l_rook[1]] == i_rook:
            if not self.square.board.getPiece(l_rook[0], l_rook[1]).has_moved:
                can_castle = True
                
                # Checks the leftmost square
                # King can castle if this square is attacked
                if board_state[king_pos[0] - 3][king_pos[1]] != 0:
                    can_castle = False
                
                # Checks squares next to the king
                # The king cannot castle if these are attacked
                # The king cannot castle if these are not empty
                for i in range(1, 3):
                    if (board_state[king_pos[0] - i][king_pos[1]] != 0) or ((king_pos[0] - i, king_pos[1]) in o_moves):
                        can_castle = False
                        break
                
                # King cannot castle if it is in check
                if self.in_check: can_castle = False

                # If all of the conditions where not met then the king cannot castle
                if can_castle: self.moves.add((king_pos[0] - 2, king_pos[1]))


        if board_state[r_rook[0]][r_rook[1]] == i_rook:
            if not self.square.board.getPiece(r_rook[0], r_rook[1]).has_moved:
                can_castle = True
                
                # Checks squares next to the king
                # The king cannot castle if these are attacked
                # The king cannot castle if these are not empty
                for i in range(1, 3):
                    if (board_state[king_pos[0] + i][king_pos[1]]) or (king_pos[0] + i, king_pos[1]) in o_moves:
                        can_castle = False
                        break

                # King cannot castle if it is in check
                if self.in_check: can_castle = False

                # All of the conditions where not met then the king cann castle
                if can_castle: self.moves.add((king_pos[0] + 2, king_pos[1]))



    def checkMoves(self, checkers):
        f_moves = set(self.moves)

        for move in self.moves:
            for p_checker in checkers:
                p_checker_pos = p_checker.getChord()
                
                # Check if the move is on the same axis
                is_ilegal = ((p_checker_pos[0] == move[0]) or (p_checker_pos[1] == move[1]) or
                            abs(p_checker_pos[0] - move[0]) == abs(p_checker_pos[1] - move[1]))
                
                is_checker = (p_checker_pos[0], p_checker_pos[1]) == (move[0], move[1])

                if is_ilegal and not is_checker: f_moves.remove(move)

        self.moves = f_moves

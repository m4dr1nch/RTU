from PIL import Image, ImageTk
import utils.images as img
import tkinter as tk

class Piece(object):
    def __init__(self, square, color):
        self.square = square
        self.color = color
        self.pinner = None
        self.moves = set()
        square.piece = self



    def getChord(self):
        return (self.square.col, self.square.row)



    def getType(self):
        return self.type



    def setIcon(self):
        self.icon = img.getImage(self.type, self.color)
        self.TK_Icon = ImageTk.PhotoImage(self.icon)
        self.square.setIcon(self.TK_Icon)



    def inRange(col, row):
        return (0 <= col <= 7) and (0 <= row <= 7)



    def inTeam(self, board_state, target_col, target_row):
        id = board_state[target_col][target_row]

        if id == 0: return False

        in_team = ((self.color == 'white') and (id % 2 == 0) or
                   (self.color == 'black') and (id % 2 != 0))
        
        if in_team: return True
        else: return False



    def addProtected(self, col, row):
        square = self.square.board.getSquare(col, row)

        if self.color == 'white':
            self.square.board.game.wh_protected.add(square.getChord())
        elif self.color == 'black':
            self.square.board.game.bl_protected.add(square.getChord())
        else: raise Exception('Incorrect color specification')



    def findMoves(self, game_state):
        self.moves.clear()

        game = self.square.board.game
        
        # If the pinned_by piece has not yet been enumerated we unset the pinned_by variable
        if self.pinner is not None and self.getType() != 'Pawn':
            if ((self.pinner.square.col > self.square.col) and
                (self.pinner.square.col > self.square.col)):
                self.pinner = None

        self.genMoves(game_state)
        
        if self.color == 'white':
            game.wh_attacking.update(self.moves)
            
            if game.bl_king.getChord() in self.moves:
                game.checkers.add(self)
        else:
            game.bl_attacking.update(self.moves)

            if game.wh_king.getChord() in self.moves:
                game.checkers.add(self)

        if self.getType() == 'Pawn':
            self.moves.update(self.inline_moves)



    def clearMoves(self):
        for move in self.moves:
            self.square.board.getSquare(move[0], move[1]).attacker = None
        self.moves.clear()



    def pinMoves(self):
        p_pinned_pos = self.getChord()
        print(self.pinner)
        p_pinner_pos = self.pinner.getChord()

        f_moves = set()
        
        # Check if the move is on the same axis as both the pinned and pinner
        for move in self.moves:
            inline = ((move[0] == p_pinner_pos[0]) and (move[0] == p_pinned_pos[0]) or
                      (move[1] == p_pinner_pos[1]) and (move[1] == p_pinned_pos[1]))
            
            diagonal = ((abs(move[0]-p_pinner_pos[0]) == abs(move[1]-p_pinner_pos[1])) and
                        (abs(move[0]-p_pinned_pos[0]) == abs(move[1]-p_pinned_pos[1])))
                        
            if inline or diagonal: f_moves.add(move)
        
        # Set the new moves
        self.moves = f_moves
        self.pinner = None



    def blockMoves(self, king, checker):
        p_checker_pos = checker.getChord()
        p_king_pos = king.getChord()

        f_moves = set()

        dist_v = abs(p_checker_pos[0]-p_king_pos[0])
        dist_h = abs(p_checker_pos[1]-p_king_pos[1])
                
        for move in self.moves:
            in_range = ((dist_v >= abs(move[0]-p_checker_pos[0])) and
                        (dist_h >= abs(move[1]-p_checker_pos[1])) and
                        (dist_v >= abs(move[0]-p_king_pos[0])) and
                        (dist_h >= abs(move[1]-p_king_pos[1])))

            inline = ((move[0] == p_checker_pos[0]) and (move[0] == p_king_pos[0]) or
                      (move[1] == p_checker_pos[1]) and (move[1] == p_king_pos[1]))

            diagonal = ((abs(move[0]-p_checker_pos[0]) == abs(move[1]-p_checker_pos[1])) and
                        (abs(move[0]-p_king_pos[0]) == abs(move[1]-p_king_pos[1])))

            if (inline or diagonal) and in_range: f_moves.add(move)

        self.moves = f_moves



    def enumerate(self, col_prefix, row_prefix, board_state):
        col = self.square.col
        row = self.square.row

        col_offset = col_prefix
        row_offset = row_prefix
        
        # Used to find pins
        in_sight = None

        while True:
            
            if (col + col_offset > 7) or (row + row_offset > 7): break
            elif (col + col_offset < 0) or (row + row_offset < 0): break

            target = board_state[col + col_offset][row + row_offset]

            if in_sight is None:
                if target == 0:
                    self.moves.add((col + col_offset, row + row_offset))
                else:
                    if self.color == 'white':
                        
                        # If target is oposite king
                        # Ads king to attacked pieces and puts it in check
                        if target == 11:
                            self.moves.add((col + col_offset, row + row_offset))
                            self.square.board.getPiece(col + col_offset, row + row_offset).in_check = True
                            break
                        
                        # If target is oposite color
                        # Ads target to attacked pieces
                        elif target % 2 != 0:
                            self.moves.add((col + col_offset, row + row_offset))
                            in_sight = self.square.board.getPiece(col + col_offset, row + row_offset)

                        # If the target is of the same color
                        else:
                            self.addProtected(col + col_offset, row + row_offset)
                            break

                    else:

                        # If target is oposite king
                        # Ads king to attacked pieces and puts it in check
                        if target == 12:
                            self.moves.add((col + col_offset, row + row_offset))
                            self.square.board.getPiece(col + col_offset, row + row_offset).in_check = True
                            break

                        # If target is oposite color
                        # Ads target to attacked pieces
                        elif target % 2 == 0:
                            self.moves.add((col + col_offset, row + row_offset))
                            in_sight = self.square.board.getPiece(col + col_offset, row + row_offset)
                        
                        # If the target is of the same color
                        else:
                            self.addProtected(col + col_offset, row + row_offset)
                            break

            else:
                if in_sight.pinner is None:
                    if ((self.color == 'white' and target == 11) or
                        (self.color == 'black' and target == 12)):
                        in_sight.pinner = self
                        self.square.board.game.pinned.add(in_sight)
                        break
                    if target != 0:
                        break
                else: break

            col_offset += col_prefix
            row_offset += row_prefix

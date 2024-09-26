import tkinter as tk
import gc

from core.pieces import *
from core.board import Board
from utils.colors import Colors

class Game(object):
    def __init__(self, panelRight):
        self.board = Board(panelRight, self)
        self.player_color = 'white'

        self.TK_Label_Results = None
        self.TK_Label_Results_Value = None

        self.wh_king = None
        self.wh_pawns = set()
        self.wh_others = set()
        self.wh_all = set()
        self.bl_king = None
        self.bl_pawns = set()
        self.bl_others = set()
        self.bl_all = set()
        self.wh_attacking = set()
        self.bl_attacking = set()
        self.wh_protected = set()
        self.bl_protected = set()
        self.pinned = set()
        self.checkers = set()
        self.frenchable = set()



    def startNewGame(self):
        # Clear game results message
        self.TK_Label_Results.config(text='')
        self.TK_Label_Results_Value.config(text='')
        
        # Flip the board according to the players side
        if ((self.player_color == 'white' and self.board.is_flipped) or
            (self.player_color == 'black' and not self.board.is_flipped)):
            self.board.flipBoard()
        
        # Unsets highlighted squares
        self.board.lastMoveColorReset()
        self.board.s_selected = None

        # Clears the board
        self.board.clear()
        
        # Basic game information
        # Used to drive the game flow
        self.has_ended = False
        self.winner = None
        self.white_to_move = True
        self.king_in_check = None
        
        self.game_state = [
            [8, 2, 0, 0, 0, 0, 1, 7],
            [4, 2, 0, 0, 0, 0, 1, 3],
            [6, 2, 0, 0, 0, 0, 1, 5],
            [10, 2, 0, 0, 0, 0, 1, 9],
            [12, 2, 0, 0, 0, 0, 1, 11],
            [6, 2, 0, 0, 0, 0, 1, 5],
            [4, 2, 0, 0, 0, 0, 1, 3],
            [8, 2, 0, 0, 0, 0, 1, 7]
        ]

        # Unsets piece information for each side
        self.wh_king = None
        self.wh_pawns.clear()
        self.wh_others.clear()
        self.wh_all.clear()

        self.bl_king = None
        self.bl_pawns.clear()
        self.bl_others.clear()
        self.bl_all.clear()
        
        # Unsets a special move called "En Passant"
        self.frenchable.clear()
        
        # Generates pieces and finds initial moves
        self.generatePieces()
        self.enumerateLegalMoves()
        
        # Runs garbage collector
        gc.collect()



    def generatePieces(self):
        for col in range(8):
            for row in range(8):
                match self.game_state[col][row]:
                    case 0:
                        Board.squares[col][row].unsetPiece()
                    case 1:
                        self.bl_pawns.add(Pawn(Board.squares[col][row], 'black'))
                    case 2:
                        self.wh_pawns.add(Pawn(Board.squares[col][row], 'white'))
                    case 3:
                        self.bl_others.add(Knight(Board.squares[col][row], 'black'))
                    case 4:
                        self.wh_others.add(Knight(Board.squares[col][row], 'white'))
                    case 5:
                        self.bl_others.add(Bishop(Board.squares[col][row], 'black'))
                    case 6:
                        self.wh_others.add(Bishop(Board.squares[col][row], 'white'))
                    case 7:
                        self.bl_others.add(Rook(Board.squares[col][row], 'black'))
                    case 8:
                        self.wh_others.add(Rook(Board.squares[col][row], 'white'))
                    case 9:
                        self.bl_others.add(Queen(Board.squares[col][row], 'black'))
                    case 10:
                        self.wh_others.add(Queen(Board.squares[col][row], 'white'))
                    case 11:
                        self.bl_king = King(Board.squares[col][row], 'black') 
                    case 12:
                        self.wh_king = King(Board.squares[col][row], 'white')



    def enumerateLegalMoves(self):
        self.wh_attacking.clear()
        self.bl_attacking.clear()
        self.wh_protected.clear()
        self.bl_protected.clear()

        self.pinned.clear()
        self.checkers.clear()

        # Clear all frenchable pieces
        # This is because "En Passant" is allowed right after a double move
        if len(self.frenchable) != 0:
            non_frenchable = set()
            for piece in self.frenchable:
                if ((piece.color == 'white' and self.white_to_move) or
                    (piece.color == 'black' and not self.white_to_move)):
                    piece.is_frenchable = False
                    non_frenchable.add(piece)
            self.frenchable -= non_frenchable

        # Finds all potentially legal moves for:
        # Queen, Rook, Bishop, Knight
        for piece in self.wh_others | self.bl_others:
            piece.findMoves(self.game_state)

        for pawn in self.wh_pawns | self.bl_pawns:
            pawn.findMoves(self.game_state)

        # Finds kings moves only after all other moves have been found
        # This is due to an edge case where the king connot
        self.wh_king.findMoves(self.game_state)
        self.bl_king.findMoves(self.game_state)

        # Modify kings moves to exclude oposite sides attacked squares
        self.wh_king.moves = self.wh_king.moves - (self.bl_attacking | self.bl_protected)
        self.bl_king.moves = self.bl_king.moves - (self.wh_attacking | self.wh_protected)

        # Find a potential check
        if self.wh_king.getChord() in self.bl_attacking:
            self.king_in_check = self.wh_king
        elif self.bl_king.getChord() in self.wh_attacking:
            self.king_in_check = self.bl_king
        else:
            self.king_in_check = None
            self.bl_king.in_check = False
            self.wh_king.in_check = False
        
        # Modify pinned piece moves
        for pinned_piece in self.pinned:
            pinned_piece.pinMoves()
        
        # Runs a routine if the king is in a check
        if self.king_in_check is not None:
            # Remove ilegal king moves
            self.king_in_check.checkMoves(self.checkers)
            
            # Get pieces that can block
            if self.king_in_check.color == 'white':
                can_block = self.wh_others | self.wh_pawns
            else:
                can_block = self.bl_others | self.bl_pawns
            
            # If the check is not a double check
            # Then enumerate blocking moves
            # Else force king moves
            if len(self.checkers) == 1:
                cant_block = set()
                for piece in can_block:
                    piece.blockMoves(self.king_in_check, next(iter(self.checkers)))
                    
                    if len(piece.moves) == 0:
                        cant_block.add(piece)
                can_block -= cant_block
            else:
                for piece in can_block:
                    piece.moves.clear()
                can_block.clear()
            
            # Check checkmate condition
            if (len(self.king_in_check.moves) == 0) and (len(can_block) == 0):
                self.TK_Label_Results.config(text='Results:')
                if ((self.player_color == 'white' and self.king_in_check.color == 'white') or
                    (self.player_color == 'black' and self.king_in_check.color == 'black')):
                    self.TK_Label_Results_Value.config(text='LOST BY CHECKMATE', fg=Colors.LIGHT_RED)
                else:
                    self.TK_Label_Results_Value.config(text='WON BY CHECKMATE', fg=Colors.LIGHT_GREEN)
        else:
            if self.white_to_move and len(self.wh_king.moves) == 0:
                for piece in self.wh_others | self.wh_pawns:
                    if len(piece.moves) != 0: return

                self.has_ended = True
                self.TK_Label_Results.config(text='Results:')
                self.TK_Label_Results_Value.config(text='DRAW BY STALEMATE', fg=Colors.LIGHT_YELLOW)
            
            if not self.white_to_move and len(self.bl_king.moves) == 0:
                for piece in self.bl_others | self.bl_pawns:
                    if len(piece.moves) != 0: return

                self.has_ended = True
                self.TK_Label_Results.config(text='Results:')
                self.TK_Label_Results_Value.config(text='DRAW BY STALEMATE', fg=Colors.LIGHT_YELLOW)

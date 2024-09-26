from PIL import Image, ImageTk
import tkinter as tk

from core.pieces import *
from core.square import Square
from utils.colors import Colors
import utils.images as img

class Board(object):
    squares = [[None] * 8 for _ in range(8)]

    s_selected = None
    
    # Used for previous move highlights
    last_A_square = None
    last_B_square = None
    
    def __init__(self, panelRight, game):
        self.is_flipped = False
        self.game = game

        self.TK_Canvas = tk.Canvas(panelRight, bg=Colors.DARK_GRAY, width=800, height=800)
        self.TK_Canvas.pack(padx=50, pady=50)

        self.dot_image = img.getImage('dot')
        self.TK_Dot_Image = ImageTk.PhotoImage(self.dot_image)
        self.TK_Null_Image = ImageTk.PhotoImage(img.getImage('null'))


        # Generates board squares
        # Grid has a different coordinate system than chess
        # We rotate the coordinates 90 degrees counter clockwise
        # The row is inverted but the column stays the same
        for grid_row, chess_row in zip(range(8), range(7, -1, -1)):
            for column in range(8):
                square = Square(self, grid_row, chess_row, column)
                square.TK_Label.bind('<Button-1>', lambda event, board=self, square=square: Board.onClick(event, board, square))
                Board.squares[column][chess_row] = square



    def getPiece(self, col, row):
        return self.squares[col][row].piece



    def getAttacker(self, col, row):
        return self.squares[col][row].attacker



    def getSquare(self, col, row):
        return self.squares[col][row]



    def flipBoard(self):
        if self.is_flipped:
            for grid_row, chess_row in zip(range(8), range(7, -1, -1)):
                for column in range(8):
                    self.squares[column][chess_row].TK_Label.grid(row=grid_row, column=column)
            self.is_flipped = False
        else:
            for grid_row, chess_row in zip(range(8), range(7, -1, -1)):
                for column in range(8):
                    self.squares[column][chess_row].TK_Label.grid(row=(8-grid_row), column=(8-column))
            self.is_flipped = True



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



    def onClick(event, board, s_clicked):
        if board.game.has_ended: return

        s_selected = board.s_selected
        s_attacker = s_clicked.attacker
        p_clicked = s_clicked.piece

        # Unselect the clicked square
        if s_selected is not None: s_selected.unselectSquare()

        # Check if clicked square is currently attacked
        if s_attacker is not None:

            # If the piece is a Pawn, King, Rook we set it as moved
            # Used for special moves (Castles and double pawn move)
            p_attacker = s_attacker.piece
            p_attacker_pos = p_attacker.getChord()
            
            
            match p_attacker.getType():
                case 'Pawn':
                    # Changes state to moved
                    # If it is a double move then we set it to frenchable
                    if not p_attacker.has_moved:
                        p_attacker.has_moved = True

                        if s_clicked.row in [3, 4]:
                            p_attacker.is_frenchable = True
                            board.game.frenchable.add(p_attacker)
                    
                    
                    if p_attacker.is_french:
                        if board.game.game_state[s_clicked.col][p_attacker_pos[1]] in [1, 2]:
                            if board.getPiece(s_clicked.col, p_attacker_pos[1]).is_frenchable:
                                if p_attacker.color == 'white':
                                    board.game.bl_pawns.remove(board.getPiece(s_clicked.col, p_attacker_pos[1]))
                                else:
                                    board.game.wh_pawns.remove(board.getPiece(s_clicked.col, p_attacker_pos[1]))
                                board.getSquare(s_clicked.col, p_attacker_pos[1]).unsetPiece()

                    # Handles pawn promotion
                    # In regular chess you can choose the piece
                    # Here it defaults to a Queen for simplicity
                    if s_clicked.row == 7:
                        board.game.wh_pawns.remove(p_attacker)
                        s_attacker.unsetPiece()
                        p_attacker.clearMoves()
                        del(p_attacker)
                        p_attacker = Queen(s_attacker, 'white')
                        board.game.wh_others.add(p_attacker)
                    elif s_clicked.row == 0:
                        board.game.bl_pawns.remove(p_attacker)
                        s_attacker.unsetPiece()
                        p_attacker.clearMoves()
                        del(p_attacker)
                        p_attacker = Queen(s_attacker, 'black')
                        board.game.bl_others.add(p_attacker)

                case 'King':
                    if not p_attacker.has_moved:
                        p_attacker.has_moved = True
                        
                        # Handles castling
                        dist = s_clicked.col - p_attacker_pos[0]
                        if abs(dist) == 2:
                            if dist == 2:
                                rook = board.getPiece(7, p_attacker_pos[1])
                                rook.square.unsetPiece()
                                board.getSquare(p_attacker_pos[0] + 1, p_attacker_pos[1]).setPiece(rook)
                            else:
                                rook = board.getPiece(0, p_attacker_pos[1])
                                rook.square.unsetPiece()
                                board.getSquare(p_attacker_pos[0] - 1, p_attacker_pos[1]).setPiece(rook)
                            rook.has_moved = True

                case 'Rook':
                    if not p_attacker.has_moved:
                        p_attacker.has_moved = True
            
            # If we have clicked a square that has a piece
            # Then we remove that piece from the gome objects sets
            if s_clicked.piece is not None:
                if s_clicked.piece.getType() == 'Pawn':
                    if s_clicked.piece.color == 'white': board.game.wh_pawns.remove(s_clicked.piece)
                    else: board.game.bl_pawns.remove(s_clicked.piece)
                else:
                    if s_clicked.piece.color == 'white': board.game.wh_others.remove(s_clicked.piece)
                    else: board.game.bl_others.remove(s_clicked.piece)


            s_clicked.setPiece(p_attacker)
            s_attacker.unsetPiece()

            # Set move colors
            board.lastMoveColor(s_selected, s_clicked)

            # Once a move is done we flip the switch and enumerate for the next position
            board.game.white_to_move = not board.game.white_to_move
            board.game.enumerateLegalMoves()
            return



        # Runs if the clicked square is not attacked but it has a piece
        if p_clicked is not None:

            # Checks if the clicked piece is allowed to be selected depending on the turn
            if board.game.white_to_move and s_clicked.piece.color == 'black': return
            if not board.game.white_to_move and s_clicked.piece.color == 'white': return

            # If no selection then we select the piece
            # If piece is the same we unselect
            # If pieces are different we switch selection
            if s_selected is None:
                s_clicked.selectSquare()
            elif s_selected == s_clicked:
                s_selected.unselectSquare()
            else:
                s_selected.unselectSquare()
                s_clicked.selectSquare()
        else:
            if s_selected is not None:
                s_selected.unselectSquare()



    def lastMoveColor(self, last_A_square, last_B_square):
        # This method adjusts the GUI colors to highlight previous move
        self.lastMoveColorReset()

        if last_A_square.color == Colors.LIGHT_VIOLET:
            last_A_square.TK_Label.config(bg=Colors.LIGHT_MOVE)
        else:
            last_A_square.TK_Label.config(bg=Colors.DARK_MOVE)

        if last_B_square.color == Colors.LIGHT_VIOLET:
            last_B_square.TK_Label.config(bg=Colors.LIGHT_MOVE)
        else:
            last_B_square.TK_Label.config(bg=Colors.DARK_MOVE)

        self.last_A_square = last_A_square
        self.last_B_square = last_B_square



    def lastMoveColorReset(self):
        # This method adjusts the GUI colors to remove highlight of the previous move
        if (self.last_A_square != None) and (self.last_B_square != None):
            self.last_A_square.TK_Label.config(bg=self.last_A_square.color)
            self.last_B_square.TK_Label.config(bg=self.last_B_square.color)
    


    def clear(self):
        # This method clears all of the pieces of the board
        for col in range(8):
            for row in range(8):
                if self.getPiece(col, row) is not None:
                    self.getPiece(col, row) == None

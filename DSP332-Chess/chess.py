#!/bin/env python
import tkinter as tk

from core.game import Game
from utils.colors import Colors

class App(tk.Tk):
    """
    App class inherited from the tkinter library.
    Used to create the widgets for the game.
    Please refer to the tkinter documentation.
    """

    def __init__(self):
        super().__init__()

        # Create window
        self.title('Chess App')
        self.geometry('1100x900')
        self.resizable(False, False)
        self.iconphoto(True, tk.PhotoImage(file='img/icon.png'))
        self.option_add('*font', 'Arial 10 bold')
        self.grid_columnconfigure(0, minsize=200, weight=2)
        self.grid_columnconfigure(1, minsize=900, weight=9)
        self.grid_rowconfigure(0, weight=1)

        # Create subframes
        TK_Panel_Left = tk.Frame(self, bg=Colors.DARK_GRAY, relief='sunken', width=200)
        TK_Panel_Left.grid(row=0, column=0, sticky='nesw')

        TK_Panel_Right = tk.Frame(self, bg=Colors.LIGHT_GRAY, relief='sunken', width=900)
        TK_Panel_Right.grid(row=0, column=1, sticky='nesw')
        
        # Create left panel widgets
        TK_Label_Title = tk.Label(TK_Panel_Left, text='Chess App', bg=Colors.DARK_GRAY, fg=Colors.WHITE, font='Arial 26 bold')
        TK_Label_Author = tk.Label(TK_Panel_Left, text='Author:', bg=Colors.DARK_GRAY, fg=Colors.WHITE, font='Arial 14 bold underline')
        TK_Label_Name = tk.Label(TK_Panel_Left, text='Mārtiņs Savickis', bg=Colors.DARK_GRAY, fg=Colors.WHITE)
        TK_Label_Nr = tk.Label(TK_Panel_Left, text='211RDB117', bg=Colors.DARK_GRAY, fg=Colors.WHITE)
        TK_Label_Group = tk.Label(TK_Panel_Left, text='10.grupa', bg=Colors.DARK_GRAY, fg=Colors.WHITE)
        TK_Label_Options = tk.Label(TK_Panel_Left, text='Options:', bg=Colors.DARK_GRAY, fg=Colors.WHITE, font='Arial 14 bold underline')
        
        game = Game(TK_Panel_Right)
        
        def toggle_side():
            if game.player_color == 'white':
                game.player_color = 'black'
                TK_Button_Toggle.config(text='Play as: Black')
            else:
                game.player_color = 'white'
                TK_Button_Toggle.config(text='Play as: White')
        
        TK_Button_Toggle = tk.Button(TK_Panel_Left, text='Play as: White', command=toggle_side, \
                bg=Colors.DARK_GRAY, fg=Colors.WHITE, \
                activebackground=Colors.LIGHT_GRAY, activeforeground=Colors.WHITE, \
                relief='solid', width=18, height=2)
        

        TK_Button_Start = tk.Button(TK_Panel_Left, text='New Game', command=game.startNewGame, \
                bg=Colors.DARK_GRAY, fg=Colors.WHITE, \
                activebackground=Colors.LIGHT_GRAY, activeforeground=Colors.WHITE, \
                relief='solid', width=18, height=2)
        
        TK_Button_Flip = tk.Button(TK_Panel_Left, text='Flip Board', command=game.board.flipBoard, \
                bg=Colors.DARK_GRAY, fg=Colors.WHITE, \
                activebackground=Colors.LIGHT_GRAY, activeforeground=Colors.WHITE, \
                relief='solid', width=18, height=2)
        
        TK_Label_Results = tk.Label(TK_Panel_Left, text='', bg=Colors.DARK_GRAY, fg=Colors.WHITE, font='Arial 14 bold underline')
        TK_Label_Results_Value = tk.Label(TK_Panel_Left, text='', bg=Colors.DARK_GRAY)

        TK_Label_Title.pack(pady=(10, 0), padx=10, anchor='w')
        TK_Label_Author.pack(padx=12, anchor='w')
        TK_Label_Name.pack(padx=12, anchor='w')
        TK_Label_Nr.pack(padx=12, anchor='w')
        TK_Label_Group.pack(padx=12, anchor='w')
        TK_Label_Options.pack(padx=12, pady=(10, 0), anchor='w')
        TK_Button_Toggle.pack(padx=12, pady=10, anchor='w')
        TK_Button_Start.pack(padx=12, pady=10, anchor='w')
        TK_Button_Flip.pack(padx=12, pady=10, anchor='w')

        TK_Label_Results.pack(padx=12, anchor='w')
        TK_Label_Results_Value.pack(padx=12, anchor='w')
        
        game.TK_Label_Results = TK_Label_Results
        game.TK_Label_Results_Value = TK_Label_Results_Value


if __name__ == '__main__':
    try:
        chess = App()
        chess.mainloop()
    except KeyboardInterrupt: exit

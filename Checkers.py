import subprocess
import sys
import numpy as np
import threading
import arcade
from UI import GameUI
from Logic import build_board,move_piece

def show_help():
    print("""
Commands:
  move A3 B4   -> Move a piece
  show         -> Display board
  restart      -> Restart game
  quit         -> Exit game
""")

def start_cli():
    cli_code = f"""
from Logic import build_board, move_piece
from UI import GameUI

board = build_board()
print('Checkers CLI ready!')
print('Type "help" for commands.')

def show_help():
    print('''
Commands:
  move A3 B4   -> Move a piece
  show         -> Display board
  restart      -> Restart game
  quit         -> Exit game
''')

show_help()

while True:
    command = input('>> ').strip().lower()
    if command == 'quit':
        print('Exiting CLI...')
        break
    elif command == 'help':
        show_help()
    elif command == 'restart':
        board = build_board()
        print('Board restarted')
    elif command.startswith('move'):
        try:
            _, start, end = command.split()
            board = move_piece(board, start, end)
            print(f'Moved {{start}} to {{end}}')
        except Exception as e:
            print('Invalid move:', e)
    elif command == 'show':
        for row in board:
            print(row)
    else:
        print('Unknown command. Type "help".')
"""

    subprocess.Popen([sys.executable, "-c", cli_code],
                     creationflags=subprocess.CREATE_NEW_CONSOLE)

play = build_board()
ui = GameUI(play)
start_cli()
ui.run()

"""threading.Thread(target=show_help).start()

arcade.run()"""
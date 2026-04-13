import threading
from UI import GameUI
from Logic import build_board, move_piece, move_options


def start_cli(ui):
    def cli_loop():
        board = ui.board

        print("Checkers CLI ready!")
        print("Commands: move A3 B4 | restart | show | quit")

        while True:
            command = input(">> ").strip().lower()

            if command == "quit":
                break

            elif command == "restart":
                board = build_board()
                ui.update_board(board)

            elif command.startswith("move"):
                try:
                    _, start, end = command.split()
                    board = move_piece(board, start, end)
                    print(board)
                    ui.update_board(board)
                except Exception as e:
                    print("Error:", e)

            elif command == "show":
                print(board)

            else:
                print("Unknown command")

    threading.Thread(target=cli_loop, daemon=True).start()


# --- RUN GAME ---
board = build_board()
ui = GameUI(board)

start_cli(ui)

ui.run()
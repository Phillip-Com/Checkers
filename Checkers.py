import threading
from UI import GameUI
from Logic import build_board, move_piece, comp_moves, convert_cords, end_game
import time

def start_cli(ui):
    def cli_loop():
        board = ui.board

        print("Checkers CLI ready!")
        print("Commands: move A3 B4 | restart | show | quit")

        while True:
            command = input(">> ").strip().lower()

            if command == "quit":
                break

            elif command.startswith("player"):
                try:
                    _, number = command.split()

                    if int(number) == 1:
                        ui.mode = "1p"
                        ui.state = "game"
                        print("Player 1 turn")
                    else:
                        ui.mode = "2p"
                        ui.state = "game"
                        print("Player 1 turn")

                except Exception as e:
                    print("Error:", e)

            elif command == "restart":
                board = build_board()
                ui.update_board(board)
                ui.state = "menu"
                ui.turn = 1

            elif ui.state != "game":
                print("Game not started. Use the menu.")
                continue

            elif command.startswith("move"):
                try:
                    _, start, end = command.split()

                    if ui.mode == "2p":
                        row, col = convert_cords(start)
                        piece = ui.board[row][col]

                    if ui.turn == 1:
                        board = move_piece(board, start, end)
                        ui.update_board(board)
                        ui.turn = -1

                        if ui.mode == "1p":
                            finish, winner = end_game(board)
                            if finish:
                                ui.result_text = winner
                                ui.state = end
                                break
                            print("Computer turn")
                            time.sleep(1.5)
                            board = comp_moves(board, -1)
                            ui.update_board(board)
                            ui.turn = 1
                            finish, winner = end_game(board)
                            if finish:
                                ui.result_text = winner
                                ui.state = end
                                break
                            print("Player 1 turn")

                    elif ui.turn == -1 and ui.mode == "2p":
                        finish, winner = end_game(board)
                        if finish:
                            ui.result_text = winner
                            ui.state = end
                            break
                        print("Player 2 turn")
                        board = move_piece(board, start, end)
                        ui.update_board(board)
                        ui.turn = 1
                        finish, winner = end_game(board)
                        if finish:
                            ui.result_text = winner
                            ui.state = end
                            break
                        print("Player 1 turn")

                except Exception as e:
                    print("Error:", e)

            elif command == "show":
                print(board)

            else:
                print("Unknown command")

    threading.Thread(target=cli_loop, daemon=True).start()


# --- RUN GAME ---
board = build_board()
ui = GameUI(board, "Checkers")

start_cli(ui)

ui.run()
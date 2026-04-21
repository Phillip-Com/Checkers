import threading
from UI import GameUI
from Logic import build_board, move_piece, comp_moves, end_game, convert_cords
import time

def start_cli(ui):
    def cli_loop():
        play = ui.board

        print("Checkers CLI ready!")
        print("Commands: "
              "\n\thelp | (Display this list of commands)"
              "\n\tmove A3 B4 | (Move a piece from start to target)"
              "\n\trestart | (Reset the board to starting position)"
              "\n\tmenu | (Return to the main menu)"
              "\n\tquit | (Stop the program)")

        while True:
            command = input(">> ").strip().lower()

            if command == "quit":
                ui.should_close = True
                break

            elif command == "help":
                print("Commands: "
                      "\n\thelp | (Display this list of commands)"
                      "\n\tmove A3 B4 | (Move a piece from start to target)"
                      "\n\trestart | (Reset the board to starting position)"
                      "\n\tmenu | (Return to the main menu)"
                      "\n\tquit | (Stop the program)")

            elif command == "restart":
                ui.state = "game"
                ui.turn = 1
                play = build_board()
                ui.update_board(play)
                print("---Board reset---\n\n")

            elif command.startswith("player"):
                try:
                    _, number = command.split()

                    if int(number) == 1:
                        ui.mode = "1p"
                    else:
                        ui.mode = "2p"
                    ui.state = "game"
                    print("Player 1 turn")

                except Exception as e:
                    print("Error:", e)

            elif command == "menu":
                ui.state = "menu"
                play = build_board()
                ui.update_board(play)
                ui.turn = 1

            elif ui.state != "game":
                print("Game not started. Use the menu.")
                continue

            elif command == "show":
                print(play)

            elif command.startswith("move"):
                try:
                    checked = True
                    while checked:
                        _, start, end = command.split()
                        check_x, check_y = convert_cords(start)
                        check_piece = play[check_x][check_y]
                        if check_piece == ui.turn or check_piece == (ui.turn * 2):
                            checked = False
                        else:
                            print("Piece targeted is not yours")
                            command = input(">> ").strip().lower()

                    if ui.turn == 1:
                        if ui.mode == "2p":
                            print("\nPlayer 2 Turn")
                        play = move_piece(play, start, end, 1)
                        ui.update_board(play)
                        ui.turn = -1

                        if ui.mode == "1p":
                            finish, winner = end_game(play, 1, 2)
                            if finish:
                                ui.default_result = winner
                                ui.state = "end"
                            print("Computer turn")
                            time.sleep(1.5)
                            play = comp_moves(play, -1)
                            ui.update_board(play)
                            ui.turn = 1
                            finish, winner = end_game(play, -1,-2)
                            if finish:
                                ui.default_result = winner
                                ui.state = "end"
                            print("Player 1 turn")

                    elif ui.turn == -1 and ui.mode == "2p":
                        finish, winner = end_game(play, -1, -2)
                        if finish:
                            ui.default_result = winner
                            ui.state = "end"
                        play = move_piece(play, start, end, 1)
                        ui.update_board(play)
                        ui.turn = 1
                        finish, winner = end_game(play, 1, 2)
                        if finish:
                            ui.default_result = winner
                            ui.state = "end"

                        print("\nPlayer 1 turn")

                except Exception as e:
                    print("Error:", e)

            else:
                print("Unknown command")

    threading.Thread(target=cli_loop, daemon=True).start()


# --- RUN GAME ---
board = build_board()
interface = GameUI(board, "Checkers")

start_cli(interface)

interface.run()
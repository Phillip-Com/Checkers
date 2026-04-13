import threading
import arcade

CELL_SIZE = 80
BOARD_SIZE = 8
WINDOW_SIZE = (BOARD_SIZE+1) * CELL_SIZE

class GameUI(arcade.Window):
    def __init__(self, board):
        super().__init__(WINDOW_SIZE, WINDOW_SIZE, "Checkers")
        arcade.set_background_color(arcade.color.BEIGE)
        self.board = board


    def update_board(self, board):
        self.board = board

    def on_draw(self):
        self.clear()
        self.draw_labels()
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0:
                    color = arcade.color.DARK_BROWN
                    x = (col + 1) * CELL_SIZE + CELL_SIZE // 100
                    y = (BOARD_SIZE - row) * CELL_SIZE + CELL_SIZE // 100
                    arcade.draw_lbwh_rectangle_filled(
                        x,
                        y,
                        CELL_SIZE,
                        CELL_SIZE,
                        color
                    )

    def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = arcade.color.BEIGE
                piece = self.board[row][col]

                if piece == 0 or piece == 9:
                    continue

                if piece == 1:
                    color = arcade.color.RED
                if piece == -1:
                    color = arcade.color.BLUE
                if piece == 2:
                    color = arcade.color.DARK_RED
                if piece == -2:
                    color = arcade.color.DARK_BLUE

                arcade.draw_circle_filled(
                    (col + 1) * CELL_SIZE + CELL_SIZE // 2,
                    (BOARD_SIZE - row) * CELL_SIZE + CELL_SIZE // 2,
                    CELL_SIZE // 3 - 2,
                    color
                )

    def draw_labels(self):
        for col in range(BOARD_SIZE):
            arcade.draw_text(
                chr(ord('A') + col),
                (col + 1) * CELL_SIZE + CELL_SIZE // 2,
                CELL_SIZE // 2,
                arcade.color.BLACK,
                font_size=40,
                anchor_x="center",
                anchor_y="center",
            )
        for row in range(BOARD_SIZE):
            arcade.draw_text(
                str(BOARD_SIZE - row),
                CELL_SIZE // 2,
                (BOARD_SIZE - row) * CELL_SIZE +CELL_SIZE // 2,
                arcade.color.BLACK,
                font_size=40,
                anchor_x="center",
                anchor_y="center",
            )
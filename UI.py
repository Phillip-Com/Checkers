import arcade

CELL_SIZE = 80
BOARD_SIZE = 8
WINDOW_SIZE = (BOARD_SIZE+2) * CELL_SIZE

class GameUI(arcade.Window):
    def __init__(self, board, title):
        super().__init__(WINDOW_SIZE, WINDOW_SIZE, title)
        arcade.set_background_color(arcade.color.IVORY)
        self.board = board
        self.should_close = False
        self.state="menu"
        self.mode = None
        self.default_result = None
        self.turn = 1

        self.title_text = arcade.Text("Checkers",300,500, arcade.color.BLACK, 40, anchor_x="center",anchor_y="center")

        self.result_text = arcade.Text("", 300, 550, arcade.color.BLACK, 30, anchor_x="center",anchor_y="center")

        self.restart = arcade.Text("Restart Game", 300,350, arcade.color.BLACK, 30,anchor_x="center")

    def update_board(self, board):
        self.board = board

    def on_draw(self):
        self.clear()

        if self.default_result is not None:
            self.result_text.text = self.default_result
            self.default_result = None

        if self.state == "menu":
            self.draw_menu()

        if self.state == "game":
            self.draw_labels()
            self.draw_board()
            self.draw_pieces()

        if self.state == "end":
            self.draw_labels()
            self.draw_board()
            self.draw_pieces()
            self.draw_end()

    def on_update(self, delta_time):
        if self.should_close:
            self.close()

    def draw_menu(self):
        arcade.draw_text(
            "CHECKERS",
            self.width // 2,
            self.height - 150,
            arcade.color.BLACK,
            50,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "Input 'player 1' for singleplayer",
            self.width // 2,
            self.height // 2 + 50,
            arcade.color.BLUE,
            30,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "Input 'player 2' for multiplayer",
            self.width//2,
            self.height // 2-50,
            arcade.color.RED,
            30,
            anchor_x="center",
            anchor_y="center"
        )

    def draw_end(self):
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
            400,400,800,800),
            (255,255,255,150)
        )
        arcade.draw_text(
            self.result_text.text,
            self.width // 2,
            self.height // 2 + 100,
            arcade.color.BLACK,
            65,
            anchor_x="center",
            anchor_y="center"
        )
        arcade.draw_text(
            "Input 'restart' to Restart",
            self.width // 2,
            self.height // 2 -50,
            arcade.color.BLACK,
            30,
            anchor_x="center"

        )
        arcade.draw_text(
            "Input 'menu' to return to the Menu",
            self.width // 2,
            self.height // 2 - 125,
            arcade.color.BLACK,
            30,
            anchor_x="center"

        )

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0:
                    color = arcade.color.BLACK
                    x = (col + 1) * CELL_SIZE + CELL_SIZE // 100
                    y = (BOARD_SIZE - row) * CELL_SIZE + CELL_SIZE // 100
                    arcade.draw_lbwh_rectangle_filled(
                        x,
                        y,
                        CELL_SIZE,
                        CELL_SIZE,
                        color
                    )
                else:
                    color = arcade.color.WHITE
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
                color = arcade.color.WHITE
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
        for col in range(BOARD_SIZE):
            arcade.draw_text(
                chr(ord('A') + col),
                (col + 1) * CELL_SIZE + CELL_SIZE // 2,
                WINDOW_SIZE - CELL_SIZE // 2,
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
        for row in range(BOARD_SIZE):
            arcade.draw_text(
                str(BOARD_SIZE - row),
                WINDOW_SIZE - CELL_SIZE // 2,
                (BOARD_SIZE - row) * CELL_SIZE +CELL_SIZE // 2,
                arcade.color.BLACK,
                font_size=40,
                anchor_x="center",
                anchor_y="center",
            )
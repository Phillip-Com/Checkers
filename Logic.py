import numpy as np
import random
import os
os.system('bash -c "ls -l"')
print(np.__version__)
x_coord = ["a", "b", "c", "d", "e", "f", "g", "h"]

#Function to place all the pieces for the board
def build_board():
    self = np.zeros((8, 8), dtype=int)
    # set spaces that aren't in play
    for i in range(8):
        for j in range(4):
            if i % 2 == 0:
                self[i][2 * j] = 9
            else:
                self[i][2 * j + 1] = 9

    # placing pieces
    for x in range(8):
        for y in range(8):
            if x < 3:
                if self[x][y] == 0:
                    self[x][y] = -1
            if x > 4:
                if self[x][y] == 0:
                    self[x][y] = 1
    return self

# Function to check if game is ended
def end_game(self):
    red_pieces = 0
    blue_pieces = 0

    for row in range(8):
        for col in range(8):
            if self[row][col] == 1 or self[row][col] == 2:
                red_pieces = red_pieces + 1

            if self[row][col] == -1 or self[row][col] == -2:
                blue_pieces = blue_pieces + 1

    if red_pieces == 0:
        return True, "Blue Wins!"
    if blue_pieces == 0:
        return True, "Red Wins!"

    return False, ""

# Function to convert board coordinates to grid coordinates
def convert_cords(self):
    col_letter = self[0]
    row_number = 8 - int(self[1:])

    for c in range(8):
        if x_coord[c] == col_letter:
            col_letter = c

    if not isinstance(col_letter, int) or row_number > 7 or row_number < 0:
        return print("Position is out of range"), ""
    elif col_letter > 7 or col_letter < 0:
        return print("Position is out of range"), ""
    else:
        return row_number, col_letter

# Function to promote a piece when on final rank
def promotion(self):
    for i in range(8):
        if self[0][i] == 1:
            self[0][i] = 2
        if self[7][i] == -1:
            self[7][i] = -2

# Function to check if player must capture
def nec_capture(board, player):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece == 0 or piece == 9:
                continue

            if player > 0 and piece > 0:
                moves = move_options(board, f"{x_coord[col]}{8-row}")
                if any(abs(r - row) == 2 for r, c in moves):
                    return True

            if player < 0 and piece < 0:
                moves = move_options(board, f"{x_coord[col]}{8-row}")
                if any(abs(r - row) == 2 for r, c in moves):
                    return True
    return False

# Function to move a piece
def move_piece(board, position, target):
    pos_x, pos_y = convert_cords(position)
    tar_x, tar_y = convert_cords(target)

    piece = board[pos_x][pos_y]

    if piece == 0 or piece == 9:
        raise ValueError("No piece at starting position")

    legal_moves = move_options(board, position)

    player = 1 if piece > 0 else -1

    must_capture = nec_capture(board, player)

    if must_capture:
        # this piece must have a capture available
        if abs(tar_x - pos_x) != 2:
            raise ValueError("you must capture when possible")

    if (tar_x, tar_y) not in legal_moves:
        raise ValueError("Illegal move")

    # --- HANDLE MOVE ---
    dx = tar_x - pos_x

    board[pos_x][pos_y] = 0
    board[tar_x][tar_y] = piece


    # capture
    if abs(dx) == 2:
        mid_x = (pos_x + tar_x) // 2
        mid_y = (pos_y + tar_y) // 2
        board[mid_x][mid_y] = 0

        current_x, current_y = tar_x, tar_y

        while capture_from(board, current_x, current_y):
            next_moves = move_options(board, coord_to_string(current_x, current_y))

            next_moves = [(r,c) for r, c in next_moves if abs(r - current_x) == 2]

            if not next_moves:
                break

            next_x, next_y = next_moves[0]

            mid_x = (current_x + next_x) //2
            mid_y = (current_y + next_y) // 2

            board[mid_x][mid_y] = 0
            board[current_x][current_y] = 0
            board[next_x][next_y] = piece

            current_x, current_y = next_x, next_y

    promotion(board)

    return board

# Function to check if there is another capture from future position
def capture_from(board, row, col):
    piece = board[row][col]

    if piece == 0 or piece == 9:
        return False

    direction = []

    if piece == -1:
        directions = [(1, 1), (1, -1)]
    elif piece == 1:
        directions = [(-1, 1), (-1, -1)]
    elif piece in (-2, 2):  # king
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for dx, dy in directions:
        nx, ny = row + dx, col + dy
        cx, cy = row + 2*dx, col + 2*dy
        if 0 <= cx < 8 and 0 <= cy < 8:
            if board[cx][cy] == 0:
                mid = board[nx][ny]
                if piece > 0 and mid < 0:
                    return True
                if piece < 0 and mid > 0:
                    return True

    return False


# Function to find places available to move
def move_options(board, position):
    x, y = convert_cords(position)
    piece = board[x][y]

    if piece == 0 or piece == 9:
        return []

    directions = []

    # movement direction
    if piece == -1:
        directions = [(1, 1), (1, -1)]
    elif piece == 1:
        directions = [(-1, 1), (-1, -1)]
    elif piece in (-2, 2):  # king
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    moves = []
    cap_moves = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        # --- NORMAL MOVE ---
        if 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] == 0:
                moves.append((nx, ny))

        # --- CAPTURE MOVE ---
        cx, cy = x + 2*dx, y + 2*dy
        if 0 <= cx < 8 and 0 <= cy < 8:
            mid = board[nx][ny]

            if board[cx][cy] == 0:
                # enemy check
                if piece > 0 and mid < 0:
                    cap_moves.append((cx, cy))
                elif piece < 0 and mid > 0:
                    cap_moves.append((cx, cy))

    if cap_moves:
        return cap_moves

    return moves

# Function to convert coords to string
def coord_to_string(row, col):
    return f"{x_coord[col]}{8-row}"

# function to collect all current move options
def all_moves(board, player):
    all_moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece == 0 or piece == 9:
                continue

            if player > 0 and piece <= 0:
                continue
            if player < 0 and piece >= 0:
                continue

            start = coord_to_string(row, col)
            moves = move_options(board, start)

            for (r, c) in moves:
                end = coord_to_string(r, c)
                all_moves.append((start, end, row, r))

    return all_moves

# Function to run computer moves
def comp_moves(board, player=-1):
    moves = all_moves(board, player)

    if not moves:
        print("Computer has no moves!")
        return board

    capture_moves = [m for m in moves if abs(m[2] - m[3]) == 2]

    if capture_moves:
        move = random.choice(capture_moves)
    else:
        move = random.choice(moves)

    start, end, _, _ = move

    print(f"Computer moves: {start} -> {end}")

    board = move_piece(board, start, end)

    return board

def run_game(self):
    if self == "start":
        print("Game started")
    elif self == "move":
        print("Move executed")
    else:
        print("Unknown command")
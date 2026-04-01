import numpy as np
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

# Function to convert board coordinates to grid coordinates
def convert_cords(self):
    a = self[0]
    b = int(self[1:]) - 1

    for c in range(8):
        if x_coord[c] == a:
            a = c

    if not isinstance(a, int) or b > 7 or b < 0:
        return print("Position is out of range"), ""
    elif a > 7 or a < 0:
        return print("Position is out of range"), ""
    else:
        return b, a

# Function to promote a piece when on final rank
def promotion(self, x, y):
    if x == 0 or x == 7:
        if self[x][y] == 1:
            self[x][y] = 2
        if self[x][y] == -1:
            self[x][y] = -2

# Function to move a piece
def move_piece(self, position, target):
    pos_x, pos_y = convert_cords(position)
    piece = self[pos_x, pos_y]
    tar_x, tar_y = convert_cords(target)
    jump_x, jump_y = pos_x + (2 * (tar_x - pos_x)), pos_y + (2 * (tar_y - pos_y))

    match piece:
        case 1 | 2:
            self[pos_x][pos_y] = 0
            if 1 <= tar_x <= 6 and 6 >= tar_y >= 1 and self[tar_x][tar_y] == -1 | -2:
                self[jump_x][jump_y] = piece
                self[tar_x][tar_y] = 0
            else:
                self[tar_x][tar_y] = piece
        case -1 | -2:
            self[pos_x][pos_y] = 0
            if 1 <= tar_x <= 6 and 6 >= tar_y >= 1 and self[tar_x][tar_y] == 1 | 2:
                self[jump_x][jump_y] = piece
                self[tar_x][tar_y] = 0
            else:
                self[tar_x][tar_y] = piece
        case _:
            print("Invalid piece for jumping")

    return self

# Function to find places available to move
def move_options(self, position):
    x, y = convert_cords(position)
    piece = self[x][y]
    directions = []
    options = []

    print(self)
    print(self[x][y])

    promotion(self, x, y)

    #
    match piece:
        case -1:
            directions = [(1, 1), (1, -1)]
        case 1:
            directions = [(-1, 1), (-1, -1)]
        case -2 | 2:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        case _:
            return print("Not a valid piece")

    #
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if self[new_x][new_y] == 0:
                options.append([new_x, new_y])

    return options

def run_game(self):
    if self == "start":
        print("Game started")
    elif self == "move":
        print("Move executed")
    else:
        print("Unknown command")
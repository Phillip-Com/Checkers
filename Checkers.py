import numpy as np
import sys

print(np.__version__)

#Declare local variables
board = np.zeros((8,8), dtype=int)
x_coord = ["A","B","C","D","E","F","G","H"]

#Function to place all the pieces for the board
def build_board(play):
    #set spaces that aren't in play
    for i in range(8):
        for j in range(4):
            if i % 2 == 0:
                play[i][2*j] = 9
            else:
                play[i][2*j+1] = 9

    #placing pieces
    for x in range(8):
        for y in range(8):
            if x < 3:
                if play[x][y] == 0:
                    play[x][y] = -1
            if x > 4:
                if play[x][y] == 0:
                    play[x][y] = 1
    return play

#Function to convert board coordinates to grid coordinates
def convert_cords(position):
    a = position[0].upper()
    b = int(position[1:])-1

    for c in range(8):
        if x_coord[c] == a:
            a = c

    if not isinstance(a, int) or b > 7 or b < 0:
        return print("Position is out of range"), ""
    elif a > 7 or a < 0:
        return print("Position is out of range"), ""
    else:
        return b, a

#Function to promote a piece when on final rank
def promotion(play,x,y):
    if x == 0 or x == 7:
        if play[x][y] == 1:
            play[x][y] = 2
        if play[x][y] == -1:
            play[x][y] = -2

#Function to move a piece
def move_piece(play,position,target):
    pos_x, pos_y = convert_cords(position)
    piece = play[pos_x, pos_y]
    tar_x, tar_y = target[0],target[1]
    jump_x, jump_y = pos_x + (2*(tar_x - pos_x)), pos_y + (2*(tar_y - pos_y))

    match piece:
        case 1 | 2:
            play[pos_x][pos_y] = 0
            if 1 <= tar_x <= 6 and 6 >= tar_y >= 1 and play[tar_x][tar_y] == -1 | -2:
                play[jump_x][jump_y] = piece
                play[tar_x][tar_y] = 0
            else:
                play[tar_x][tar_y] = piece
        case -1 | -2:
            play[pos_x][pos_y] = 0
            if 1 <= tar_x <= 6 and 6 >= tar_y >= 1 and play[tar_x][tar_y] == 1 | 2:
                play[jump_x][jump_y] = piece
                play[tar_x][tar_y] = 0
            else:
                play[tar_x][tar_y] = piece
        case _:
            print("Invalid piece for jumping")

#Function to find places available to move
def move_options(play,position):
    x, y = convert_cords(position)
    piece = play[x][y]
    directions = []
    options = []

    print(play)
    print(play[x][y])

    promotion(play,x,y)

    #
    match piece:
        case -1:
            directions = [(1,1),(1,-1)]
        case 1:
            directions = [(-1,1),(-1,-1)]
        case -2 | 2:
            directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        case _:
            return print("Not a valid piece")

    #
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            if play[new_x][new_y] == 0:
                options.append([new_x,new_y])

    return options

def run_game(command):
    if command == "start":
        print("Game started")
    elif command == "move":
        print("Move executed")
    else:
        print("Unknown command")

run_game("start")

def main():
    if len(sys.argv) < 2:
        print("usage: python3 Checkers.py <command>")
        return

    command = sys.argv[1]
    run_game(command)

if __name__ == "__main__":
    main()
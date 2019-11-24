import sys
import random

#Shamlessly taken from simpletilegame.py
def parse_input_file(input_file):
    board = []  # 2D array
    pieces = {} # hashmap of 2D arrays
    key_count = -1
    with open(input_file, 'r') as f:
        line = f.readline().strip('\n')
        #print(line)
        while line:
            key_count += 1
            curr_fig = []
            while line != "":
                curr_fig.append(list(line))
                line = f.readline().strip('\n')
            #print(curr_fig)
            line = f.readline().strip('\n')
            pieces[key_count] = curr_fig
        board = pieces.pop(key_count)
        #print(board)
    f.close()
    return board, pieces

# Prints board. Mainly for debugging purposes
def print_board(board):
    for line in board:
        for char in line:
            print(char, end="")
        print()
    print()

# Prints piece. Mainly for debugging purposes
def print_piece(piece):
    for line in piece:
        for char in line:
            print(char, end="")
        print()
    print()
# Takes in a piece and a number of iterations. 
# Returns the piece rotated 90 degrees to the right iteration times.
def rotate_piece(piece, times):
    finalPiece = piece
    for i in range(times%4):
        newPiece = []
        height = len(finalPiece)
        length = len(finalPiece[0])
        for i in range(length):
            newPieceLine = []
            for j in range(height):
                newPieceLine.append(finalPiece[height-j-1][i])
            newPiece.append(newPieceLine)
        finalPiece = newPiece
    return finalPiece

# Takes in a board, piece, x and y location. Returns if piece will fit at 
# location (x,y)
def will_piece_fit(board, piece, loc_X, loc_Y):
    for x in range(len(piece)):
        for y in range(len(piece[0])):
            print(piece[x][y], "?=", board[loc_X+x][loc_Y+y])
            if piece[x][y]!=board[loc_X+x][loc_Y+y] and piece[x][y]!=" ":
                return False
    return True
# Takes in a board, piece, x and y location. Puts piece in place on board.
# Represents spaces that are taken with " "
def put_piece_in_place(board, piece, loc_X, loc_Y):
    new_board = board
    for x in range(len(piece)):
        for y in range(len(piece[0])):
            if piece[x][y]!=" ":
                new_board[loc_X+x][loc_Y+y]=" "
    return new_board

# Takes in a board. Returns if it is filled
def is_board_full(board):
    for line in board:
        for spot in line:
            if spot != " ":
                return False
    return True

# Takes in a piece. Returns a
def find_spot_for_piece(board, piece):
    for x in range(len(board)):
        for y in range(len(board[0])):
            for rotation in range(3):
                working_piece = rotate_piece(piece, rotation)
                if will_piece_fit(board, working_piece, x, y):
                    return x,y,rotation,True
    return None, None, None, False

def brute_force(board, pieces):
    while True:
        available_pieces = []
        for piece in pieces:
            available_pieces.append(pieces[piece])
        working_board = board
        solution = []    
        for piece in pieces:
            currPiece = available_pieces[random.randint(0, len(available_pieces)-1)]
            x_placement, y_placement, rotation, is_placable = find_spot_for_piece(working_board, currPiece)
            print(x_placement, y_placement, rotation, is_placable)
            if is_placable:
                solution.append([currPiece,x_placement, y_placement, rotation])
                working_board = put_piece_in_place(working_board, rotate_piece(currPiece, rotation), x_placement, y_placement)
                available_pieces.remove(currPiece)
            else:
                break
        
        return solution

            
            

myBoard, myPieces = parse_input_file(sys.argv[1])

print_board(myBoard)
for piece in myPieces:
    print_piece(myPieces[piece])

print(brute_force(myBoard, myPieces))
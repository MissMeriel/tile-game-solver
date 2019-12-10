import sys
import copy
import more_itertools
import time

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

# Takes in a piece and returns it flipped from the top to bottom (not left to right)
def flip_piece(piece):
    flipped_piece = copy.deepcopy(piece)
    flipped_piece.reverse()
    return flipped_piece

# Takes in a board, piece, x and y location. Returns if piece will fit at 
# location (x,y)
def will_piece_fit(board, piece, loc_X, loc_Y):
    # print(len(piece[0])+loc_Y)
    # print(len(piece)+loc_X)
    # print(len(board[0]))
    # print(len(board))
    if len(piece[0])+loc_Y > len(board[0]) or len(piece)+loc_X > len(board):
        return False
    for x in range(len(piece)):
        for y in range(len(piece[x])):
                #print(piece[x][y], "?=", board[loc_X+x][loc_Y+y])
                if piece[x][y]!=board[loc_X+x][loc_Y+y] and piece[x][y]!=" ":
                    return False
    return True
# Takes in a board, piece, x and y location. Puts piece in place on board.
# Represents spaces that are taken with " "
def put_piece_in_place(board, piece, loc_X, loc_Y, key):
    for x in range(len(piece)):
        for y in range(len(piece[x])):
            if piece[x][y]!=" ":
                board[loc_X+x][loc_Y+y]=key
    return board

# Takes in a board. Returns if it is filled
def is_board_full(board):
    for line in board:
        for spot in line:
            if spot != " ":
                return False
    return True

# Takes in a piece. Returns a
def find_spot_for_piece(board, piece):
    for y in range(len(board)):
        for x in range(len(board[0])):
            #for rotation in range(4):
                #for flip in range(2):
                    #if flip:
                    #    working_piece = flip_piece(rotate_piece(piece, rotation))
                    #else:
                        #working_piece = rotate_piece(piece, rotation)
            if will_piece_fit(board, piece, x, y):
                        #return x,y,rotation,flip,True
                return x,y,0,0,True
    return None, None, None, None, False

def is_spot_for_piece(board, piece):
    for x in range(len(board)):
        for y in range(len(board[x])):
            if will_piece_fit(board, piece, x, y):
                return True
    return False

# This is a helper function that finds how spots are in a piece
# It returns a dictionary where the keys are the type of piece and the values
# are the number of that type of piece. So for the piece "XOX", it would return
# {"X":2, "O":1}
def num_spots_in_piece(piece):
    num_spots={}
    for line in piece:
        for spot in line:
            if spot != " ":
                if spot not in num_spots:
                    num_spots[spot] = 1
                else:
                    num_spots[spot]+=1
    return num_spots

# This is a helper function that checks if a set of pieces has the correct
# number of each type of piece to fill a board. If a board has 20 "X"s and 
# 15 "Y"s, a valid solution must have pieces that have 15 "Y"s and 20 "X"s
def has_necessary_num_pieces(board, num_spots_in_pieces):
    num_spots={}
    for line in board:
        for spot in line:
            if spot != " ":
                if spot not in num_spots:
                    num_spots[spot] = 1
                else:
                    num_spots[spot]+=1
    
    return num_spots_in_pieces == num_spots

# This function takes in the board and the given pieces and returns which set
# of pieces may be a viable solution set.
# Using the library more_itertools, we get the powerset of pieces. This allows
# us to find which set of pieces has the correct number of types of spots.
# For each set in the powerset, it checks if the pieces meet this condition.
# If they do, they are added to the set of plausible sets. The set of plausible
# sets are then returned
def get_plausible_sets(board, pieces):
    piece_power_set = more_itertools.powerset(pieces)
    
    plausibleSets=[]
    for aSet in piece_power_set:
        sum_of_set = {}
        for item in aSet:
            this_pieces_spots = num_spots_in_piece(pieces[item])
            for piece_type in this_pieces_spots:
                if piece_type in sum_of_set:
                    sum_of_set[piece_type]+=this_pieces_spots[piece_type]
                else:
                    sum_of_set[piece_type]=this_pieces_spots[piece_type]
        if has_necessary_num_pieces(board, sum_of_set):
            plausibleSet = {}
            myIter = 0
            for item in aSet:
                plausibleSet[myIter] = pieces[item]
                myIter+=1
            plausibleSets.append(plausibleSet) 
    return plausibleSets  

# This is the function that calls the correct type of depth first search
# (I.E. includes rotations or flips of pieces)
# It returns whatever solutions it finds
def dfs(board, pieces, choice):
    start = time.time()
    solutions = []
    available_spots = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] != " ":
                available_spots.append([x,y])
            
    if choice == 0:
        dfs_helper(board, pieces, 0, [], solutions, available_spots, start)
    elif choice == 1:
        dfs_helper_with_rotation(board, pieces, 0, [], solutions, available_spots, start)
    elif choice == 2:
        dfs_helper_with_flip(board, pieces, 0, [], solutions, available_spots, start)
    elif choice == 3:
        dfs_helper_with_rotation_and_flip(board, pieces, 0, [], solutions, available_spots, start)
    print("Time to search all solutions:", time.time()-start)
    return solutions

# Base DFS helper. It takes in a board, a set of pieces, the depth in the DFS
# tree it is at, the current solution that is being built, and the set of solutions.
# If the board it is given has been solved, then it returns adds the current solution 
# it was given to the set of solutions. 
# If the board hasn't been solved and the depth is less thanthe number of pieces, then 
# there are still pieces to be placed. For each spot on the board, it attempts to place
# the next piece. If it will fit at that spot, it places it in a copy of the board, adds
# to the current solution, and finally calls itself with the new board, the pieces, a depth
# one higher, the newly made current solution, and the solution set.
def dfs_helper(board, pieces, depth, currSolution, solutions, available_spots, start):
    #print(is_board_full(board))
    if is_board_full(board):
        solutions.append(currSolution)
        if len(solutions) == 1:
            print("Time to find one solution:", time.time()-start)

    elif depth < len(pieces):
        nonvalid=False
        for piece in pieces:
            if not is_spot_for_piece(board, pieces[piece]) and piece > depth:
                nonvalid = True
        for spot in available_spots:
            if nonvalid:
                break
            currPiece = pieces[depth]
            new_board = copy.deepcopy(board)
            if will_piece_fit(new_board, currPiece, spot[0], spot[1]):
                new_board = put_piece_in_place(new_board, currPiece, spot[0], spot[1], " ")
                new_curr_solution = currSolution+[[spot[0],spot[1],pieces[depth],0,0]]
                new_available_spots = copy.deepcopy(available_spots)
                # new_available_spots.remove([spot[0],spot[1]])
                dfs_helper(new_board, pieces, depth+1, new_curr_solution, solutions, new_available_spots, start)

# DFS helper that includes piece rotations. This is very similar to the base helper.
# It now also attempts to place a piece in a board after rotating it 0, 90, 180, and 270
# degrees.  
def dfs_helper_with_rotation(board, pieces, depth, currSolution, solutions, available_spots, start):
    #print("new search started")
    if is_board_full(board):
        solutions.append(currSolution) 

    elif depth < len(pieces):
        nonvalid=False
        for piece in pieces:
            no_solve = 0
            for rotation in range(4):
                if not is_spot_for_piece(board, rotate_piece(pieces[piece],rotation)) and piece > depth:
                    no_solve+=1
                nonvalid = (no_solve == 4)
                
        for spot in available_spots:
            if nonvalid:
                break
            for rotation in range(4):
                currPiece = rotate_piece(pieces[depth],rotation)
                new_board = copy.deepcopy(board)
                if will_piece_fit(new_board, currPiece, spot[0], spot[1]):
                    new_board = put_piece_in_place(new_board, currPiece, spot[0], spot[1], " ")
                    new_curr_solution = currSolution+[[spot[0],spot[1],pieces[depth],rotation,0]]
                    new_available_spots = copy.deepcopy(available_spots)
                    new_available_spots.remove([spot[0],spot[1]])
                    dfs_helper_with_rotation(new_board, pieces, depth+1, new_curr_solution, solutions, new_available_spots, start)

# DFS helper that includes piece flips. This is very similar to the base helper.
# It now also attempts to place a piece in a board after flipping it. So a piece
# X                             XX
# X   would be flipped to be    X
# XX                            X
def dfs_helper_with_flip(board, pieces, depth, currSolution, solutions, available_spots, start):
    #print(is_board_full(board))
    if is_board_full(board):
        solutions.append(currSolution) 

    elif depth < len(pieces):
        nonvalid=False
        for piece in pieces:
            if not is_spot_for_piece(board, pieces[piece]) and not is_spot_for_piece(board, flip_piece(pieces[piece])) and piece > depth:
                nonvalid=True
                
        for spot in available_spots:
            if nonvalid:
                break
            for flip in range(2):
                if flip:
                    currPiece = flip_piece(pieces[depth])
                else:
                    currPiece = pieces[depth]
                new_board = copy.deepcopy(board)
                if will_piece_fit(new_board, currPiece, spot[0], spot[1]):
                    new_board = put_piece_in_place(new_board, currPiece, spot[0], spot[1], " ")
                    new_curr_solution = currSolution+[[spot[0],spot[1],pieces[depth],0, flip]]
                    new_available_spots = copy.deepcopy(available_spots)
                    new_available_spots.remove([spot[0],spot[1]])
                    dfs_helper_with_flip(new_board, pieces, depth+1, new_curr_solution, solutions, new_available_spots, start)

# This DFS helper combines the previous two by allowing both flips and rotations.
def dfs_helper_with_rotation_and_flip(board, pieces, depth, currSolution, solutions, available_spots, start):
    #print(is_board_full(board))
    if is_board_full(board):
        solutions.append(currSolution) 
    elif depth < len(pieces):
        nonvalid=False
        for piece in pieces:
            no_solve = 0
            for rotation in range(4):
                if not is_spot_for_piece(board, pieces[piece]) and not is_spot_for_piece(board, flip_piece(pieces[piece])) and piece > depth:
                    no_solve+=1
                nonvalid = (no_solve == 4)

            if nonvalid:
                break
            for spot in available_spots:
                for rotation in range(4):
                    for flip in range(2):
                        if flip:
                            currPiece = rotate_piece(flip_piece(pieces[depth]),rotation)
                        else:
                            currPiece = rotate_piece(pieces[depth],rotation)
                        #print("At depth:", depth)
                        #print(x,y)
                        #print_piece(currPiece)
                        new_board = copy.deepcopy(board)
                        #print_board(new_board)
                        if will_piece_fit(new_board, currPiece, spot[0], spot[1]):
                            new_board = put_piece_in_place(new_board, currPiece, spot[0], spot[1], " ")
                            new_curr_solution = currSolution+[[spot[0],spot[1],pieces[depth],rotation, flip]]
                            new_available_spots = copy.deepcopy(available_spots)
                            new_available_spots.remove([spot[0],spot[1]])
                            dfs_helper_with_rotation_and_flip(new_board, pieces, depth+1, new_curr_solution, solutions, available_spots, start)

def order_pieces_by_size(myPieces):
    pieces = myPieces.values()
    pieces = sorted(pieces, key=lambda piece: len(piece) * len(piece[0]), reverse=True)
    myPieces = dict()
    for i in range(len(pieces)):
        myPieces.update({i: pieces[i]})
    #print("myPieces={}".format(myPieces))
    return myPieces

def fill_board_with_solution(board, solution):
    key = ord('a')
    for piece in solution:
        placed_piece = copy.deepcopy(piece[2])
        if piece[4]:
            placed_piece = flip_piece(placed_piece)
        placed_piece = rotate_piece(placed_piece, piece[3])
        put_piece_in_place(board, placed_piece, piece[0], piece[1], chr(key))
        #print_board(board)
        key+=1

def solutions_are_isomorphic(board1, board2):
    for rotation in range(4):
        for flip in range(2):
            if flip:
                if board1 == flip_piece(rotate_piece(board2, rotation)):
                    return True
            else:
                if board1 == rotate_piece(board2, rotation):
                    return True
    return False
     

def main():
    myBoard, myPieces = parse_input_file(sys.argv[1])
    # print_board(myBoard)
    # for piece in myPieces:
    #     print_piece(myPieces[piece])

    # print(brute_force(myBoard, myPieces))
    #print_board(myBoard)
    #print(myPieces)
    #for piece in myPieces:
    #    print_piece(myPieces[piece])
    #    print_piece(flip_piece(myPieces[piece]))

    plausibleSets = get_plausible_sets(myBoard, myPieces)
    #print(len(plausibleSets))


    allSolutions = []
    start = time.time()
    #counter=0
    if plausibleSets:
        for plausibleSet in plausibleSets:
            #print(counter)
            #counter+=1
            ### No solution found to trivial.txt with choice=2
            some_solutions = (dfs(myBoard, plausibleSet, 3))
            if some_solutions!=[]:
                allSolutions.append(some_solutions)
    else:
        print("There are no plausible sets")
    print(time.time()-start)

    myPieces=order_pieces_by_size(myPieces)
    if allSolutions!=[]:
        print("There is/are", len(allSolutions[0]), "solution(s).")
        solved_board = copy.deepcopy(myBoard)
        fill_board_with_solution(solved_board, allSolutions[0][0])
        prunedSolutions = [solved_board]
        for solution in allSolutions[0]:
            new_solution = copy.deepcopy(myBoard)
            fill_board_with_solution(new_solution, solution)
            validSolution = True
            for non_isomorphic_solution in prunedSolutions:
                if solutions_are_isomorphic(new_solution, non_isomorphic_solution):
                    validSolution =False
                    break
            if validSolution:
                prunedSolutions.append(new_solution)

        print("There is/are", len(prunedSolutions), "non-isomorphic solution(s).")
        for aSolution in prunedSolutions:
            print_board(aSolution)
    else:
        print("There are no solutions!")

main()
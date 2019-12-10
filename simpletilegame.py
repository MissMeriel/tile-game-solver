"""memory puzzle - gui version using classes
    simple implementation of classic game memoty tile puzzle
    for animation and graphics i use turtle module 
"""
import turtle, random, time
import sys

#-- constants 
tile = 100 # orig 100
window_width = 1000
width = 500
height = 800
flip = False
board_width = 0
board_height = 0
board = []
STAMP_SIZE = 20.0

#-- screen setup 
screen = turtle.Screen()
screen.setup(window_width, height, 700)
screen.bgcolor("black")
screen.tracer(1)

#-- class Game maps graphic attribs to game
class Game(turtle.Turtle):
    def __init__(self):
        global board_height, board_width, board, tile, width
        board_width = len(board[0])
        board_height = len(board)
        #-- module attributes
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.penup()
        self.shape("square")
        ss = tile / STAMP_SIZE
        self.shapesize(ss)
        #self.setpos(-250 -250 + tile/2, 250 - tile/2)
        self.setpos(-250 - 245 + tile / 2, 245 - tile / 2)
        # fastest=10, slowest=1
        self.speed(8)
        #-- game attributes
        self.items = board
        self.grid = [] #-- to find the position of each tile
        self.temp_selected = []
        self.temp_coordinates = []
        self.count = 0
        self.correct = 0
        self.piece_grid = dict() #-- to find the location of pieces

    def game_setup(self, _board):
        global board_height, board_width, board, tile, width
        board = _board
        board_width = len(board[0])
        board_height = len(board)
        maxdim = board_width
        if board_width < board_height:
            maxdim = board_height
        tile = width / float(board_width)
        self.items = board

    #-- print the board to stdout
    def print_items(self):
        for r in range(len(self.items)):
            time.sleep(0.10)
            for c in range(len(self.items[0])):
                print(self.items[r][c], end ="")
            print()

    #-- map colors to representation in input file
    def get_color(self, marker):
        if marker == "a":
            self.fillcolor("white")
        elif marker == "b":
            self.fillcolor("blue")
        elif marker == "%":
            self.fillcolor("orange")
        elif marker == "#":
            self.fillcolor("red")
        elif marker == "X":
            self.fillcolor("green")
        elif marker == "O":
            self.fillcolor("yellow")
        elif marker == "g":
            self.fillcolor("light green")
        elif marker == "h":
            self.fillcolor("pink")
        elif marker == "s":
            self.fillcolor("lightblue")
        elif marker == "o":
            self.fillcolor("gold")
        elif marker == " ":
            self.fillcolor("black")
        elif marker == "Z":
            self.fillcolor("seashell")

    def get_outline_color(self, marker):
        self.shapesize(outline=5)
        if marker == "a":
            self.pencolor("pink")
        elif marker == "b":
            self.pencolor("magenta")
        elif marker == "c":
            self.pencolor("gold")
        elif marker == "d":
            self.pencolor("brown")
        elif marker == "e":
            self.pencolor("violet")
        elif marker == "f":
            self.pencolor("lightblue")
        elif marker == "g":
            self.pencolor("gray")
        elif marker == "h":
            self.pencolor("darkgreen")
        elif marker == "i":
            self.pencolor("maroon")
        elif marker == "j":
            self.pencolor("light green")
        elif marker == "k":
            self.pencolor("chocolate")
        elif marker == "l":
            self.pencolor("turquoise")

    #-- draw the graphical board according to input
    def draw_board(self):
        ss = tile / STAMP_SIZE
        self.shapesize(ss)
        self.setpos(-250 - 245 + tile / 2, 245 - tile / 2)
        spacer = tile+4
        for r in range(len(self.items)):
            for c in range(len(self.items[0])):
                self.get_color(self.items[r][c])
                self.stamp()
                int(self.xcor())
                int(self.ycor())
                ### TODO: CHANGE TO 2D ARRAY
                self.grid.append((self.xcor(), self.ycor()))#-- keep a track of position of each tile
                self.forward(spacer)
            self.back(spacer * board_width)
            self.right(90)
            self.forward(spacer)
            self.left(90)

    def draw_pieces(self, pieces):
        # get max height of pieces
        max_height = get_max_height(pieces)
        width_offset = self.grid[0][-1]
        #self.setpos(0 + tile/2, width_offset - tile/2)
        self.setpos(75 + tile*1, width_offset - tile / 2)
        self.shapesize(1)
        minitile=10
        ss = minitile / STAMP_SIZE
        self.shapesize(ss)
        for key in pieces:
            p = pieces[key]
            for r in range(len(p)):
                for c in range(len(p[0])):
                    self.get_color(p[r][c])
                    self.stamp()
                    int(self.xcor())
                    int(self.ycor())
                    self.forward(minitile)
                self.back(minitile * len(p[0]))
                self.right(90)
                self.forward(minitile)
                self.left(90)
            curr_pos = self.pos()
            if (self.ycor() < 0 and abs(self.ycor())+ minitile * max_height > self.grid[0][-1]):
                self.setx(self.xcor() + minitile * max_height)
                self.sety(250 - tile/2)
            self.right(90)
            self.forward(2 * minitile)
            self.left(90)

    #-- locate each tile in board
    def get_coordinate(self, r,c):
        if (r,c) == (0,0):
            return self.grid[0]
        elif (r,c) == (0,1):
            return self.grid[1]
        elif (r,c) == (0,2):
            return self.grid[2]
        elif (r,c) == (0,3):
            return self.grid[3]
        elif (r,c) == (1,0):
            return self.grid[4]
        elif (r,c) == (1,1):
            return self.grid[5]
        elif (r,c) == (1,2):
            return self.grid[6]
        elif (r,c) == (1,3):
            return self.grid[7]
        elif (r,c) == (2,0):
            return self.grid[8]
        elif (r,c) == (2,1):
            return self.grid[9]
        elif (r,c) == (2,2):
            return self.grid[10]
        elif (r,c) == (2,3):
            return self.grid[11]
        elif (r,c) == (3,0):
            return self.grid[12]
        elif (r,c) == (3,1):
            return self.grid[13]
        elif (r,c) == (3,2):
            return self.grid[14]
        elif (r,c) == (3,3):
            return self.grid[15]
        elif (r,c) == (4,0):
            return self.grid[16]
        elif (r,c) == (4,1):
            return self.grid[17]
        elif (r,c) == (4,2):
            return self.grid[18]
        elif (r,c) == (4,3):
            return self.grid[19]

    def draw_solution(self, solution):
        global board_width, board_height, tile
        marker_set = set()
        self.shapesize((tile / STAMP_SIZE))
        for row in range(len(solution)):
            for col in range(len(solution[row])):
                marker = solution[row][col]
                grid_number = row * board_width + col
                tile_coords = self.grid[grid_number]
                self.get_outline_color(marker)
                self.get_color(board[row][col])
                self.setpos(tile_coords)
                self.stamp()
        time.sleep(2)

def get_max_height(pieces):
    height = 0
    for key in pieces.keys():
        p = pieces[key]
        if(len(p) > height):
            height =len(p)
    return height

def parse_input_file(input_file):
    board = []  # 2D array
    pieces = {} # hashmap of 2D arrays
    key_count = -1
    with open(input_file, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            key_count += 1
            curr_fig = []
            while line != "":
                curr_fig.append(list(line))
                line = f.readline().strip('\n')
            line = f.readline().strip('\n')
            pieces[key_count] = curr_fig
        board = pieces.pop(key_count)
    f.close()
    return board, pieces

#-- main function 
def main():
    global board, board_width, board_height, tile
    # -- creating class object and calling methods
    input_file = sys.argv[1]
    board, pieces = parse_input_file(input_file)
    try:
        flip_flag = sys.argv[2]
        if flip_flag == "flip":
            flip = True
    except:
        flip = False
    board_width = len(board[0])
    board_height = len(board)
    print("board size: {},{}".format(board_height, board_width))
    #-- game setup
    game = Game()
    game.game_setup(board)
    game.print_items()
    game.draw_board()
    game.draw_pieces(pieces)
    while True:
        user_input = input("Press any key to exit:")
        if user_input:
            exit()
        turtle.mainloop() #-- creates the main loop for turtle screen


if __name__ == "__main__":
    main()
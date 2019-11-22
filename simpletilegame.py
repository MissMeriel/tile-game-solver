"""memory puzzle - gui version using classes
    simple implementation of classic game memoty tile puzzle
    for animation and graphics i use turtle module 
"""
import turtle, random, time
import sys

#-- constants 
tile = 100
window_width = 1000
width = 500
height = 500
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

#-- class Game holding graphic attribs and game attribs
class Game(turtle.Turtle):
    def __init__(self):
        #-- module attributes
        turtle.Turtle.__init__(self)
        self.hideturtle()
        self.penup()
        self.shape("square")
        ss = tile / STAMP_SIZE
        self.shapesize(ss)
        self.setpos(-250 -250 + tile/2, 250 - tile/2)
        self.speed(4)
        #-- game attributes
        self.items = board
        self.grid = [] #-- to find the position of each tile
        self.temp_selected = []
        self.temp_coordinates = []
        self.count = 0
        self.correct = 0 

    #-- print the board to stdout
    def print_items(self):
        for r in range(len(self.items)):
            time.sleep(0.10)
            for c in range(len(self.items[0])):
                print(self.items[r][c], end ="")
            print()

    #-- map colors to representation in input file
    def get_color(self, r,c):
        if self.items[r][c] == "a":
            self.fillcolor("white")
        elif self.items[r][c] == "b":
            self.fillcolor("blue")
        elif self.items[r][c] == "%":
            self.fillcolor("orange")
        elif self.items[r][c] == "#":
            self.fillcolor("red")
        elif self.items[r][c] == "X":
            self.fillcolor("green")
        elif self.items[r][c] == "O":
            self.fillcolor("yellow")
        elif self.items[r][c] == "g":
            self.fillcolor("light green")
        elif self.items[r][c] == "h":
            self.fillcolor("pink")
        elif self.items[r][c] == "s":
            self.fillcolor("lightblue")
        elif self.items[r][c] == "o":
            self.fillcolor("gold")
        elif self.items[r][c] == " ":
            self.fillcolor("black")

    #-- map colors to representation in input file
    def get_color2(self, marker):
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

    #-- draw the graphical board according to input
    def draw_colors(self):
        for r in range(len(self.items)):
            for c in range(len(self.items[0])):
                self.get_color(r,c)
                self.stamp()
                int(self.xcor())
                int(self.ycor())
                self.grid.append((self.xcor(), self.ycor()))#-- keep a track of position of each tile
                self.forward(tile)
            self.back(tile * board_width)
            self.right(90)
            self.forward(tile)
            self.left(90)

    def draw_pieces(self, pieces):
        # get max height of pieces
        max_height = get_max_height(pieces)
        self.setpos(0 + tile/2, 250 - tile/2)
        self.shapesize(1)
        minitile=10
        ss = minitile / STAMP_SIZE
        self.shapesize(ss)
        for key in pieces:
            p = pieces[key]
            print(p)
            for r in range(len(p)):
                for c in range(len(p[0])):
                    #print("marker:{} r:{} c:{}".format(p[r][c], r, c))
                    self.get_color2(p[r][c])
                    self.stamp()
                    int(self.xcor())
                    int(self.ycor())
                    self.grid.append((self.xcor(), self.ycor()))  # -- keep a track of position of each tile
                    self.forward(minitile)
                self.back(minitile * len(p[0]))
                self.right(90)
                self.forward(minitile)
                self.left(90)
            curr_pos = self.pos()
            #if(abs(self.xcor()) > width/2.0):
            #    self.setx(0 + tile/2)
            #    print("RESET X")
            if (self.ycor() < 0 and abs(self.ycor())+ minitile * max_height > height / 2.0):
                self.setx(self.xcor() + minitile * max_height)
                self.sety(250 - tile/2)
                print("RESET Y")
            self.right(90)
            self.forward(2 * minitile)
            self.left(90)

    #-- covers the tiles by stamping the gray color on them 
    def draw_cover(self):
        self.fillcolor("gray")
        self.setpos(-200, 200)
        for r in range(len(self.items)):
            for c in range(len(self.items[0])):
                self.stamp()
                self.forward(tile)
            self.back(tile*4)
            self.right(90)
            self.forward(tile)
            self.left(90)
        self.reset_first_click()
    #-- acording to grid list we can locate the exact position of each tile
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
    #-- metod to select the first tile
    #-- keeps  a track of temporary coordinates, and selected item
    def first(self, x,y):
        self.temp_coordinates.clear()
        self.temp_selected.clear()
        #-- converting cartesian board to screen (row, column)
        c = int(x+(width/2)) // tile
        r = int(-y +(height/2)) //tile
        self.get_color(r,c)
        self.goto(self.get_coordinate(r,c))
        self.stamp()
        self.temp_selected.append(self.items[r][c])
        self.temp_coordinates.append(self.pos())
        self.reset_second_click()
    #-- metod to select the second tile
    #-- keeps  a track of temporary coordinates, and selected item
    def second(self, x,y):
        c = int(x+(width/2)) // tile
        r = int(-y +(height/2)) //tile
        self.get_color(r,c)
        self.goto(self.get_coordinate(r,c))
        if self.pos() == self.temp_coordinates[0]:
            print("this is the first color, choose second color!")
        else:
            self.stamp()
            self.temp_selected.append(self.items[r][c])
            self.temp_coordinates.append(self.pos())
            self.check()
    #-- checks if two selected tiles are match and reset the temporary trackers    
    def check(self):
        if self.temp_selected[0] == self.temp_selected[1]:
            print("correct")
            self.correct += 1
            if self.correct == 10:               
                print("You solve the puzzle with: ", self.correct + self.count, "moves.")
            self.reset_first_click()
        else:
            self.count +=1
            self.fillcolor("gray")
            for coordinate in self.temp_coordinates:
                self.goto(coordinate)
                self.stamp()
                self.reset_first_click()
    #-- reseting the mouse event for first and second selection 
    def reset_first_click(self):
        turtle.onscreenclick(self.first)    
    def reset_second_click(self):
        turtle.onscreenclick(self.second)

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
    maxdim = board_width
    if board_width < board_height:
        maxdim = board_height
    tile = width / float(board_width)
    #-- game setup
    game = Game()
    game.print_items()
    game.draw_colors()
    game.draw_pieces(pieces)
    while True:
        user_input = input("Press any key to exit:")
        if user_input:
            exit()
        turtle.mainloop() #-- creates the main loop for turtle screen


if __name__ == "__main__":
    main()
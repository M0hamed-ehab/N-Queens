import random
import time
import GUI
import globals
########################################################--Board Class--########################################################
class Board:
    def __init__(self, N, start= -1):
        self.N = N
        self.board = [[0] * N for _ in range(N)]
        self.timing=time.time()
        if start == -1:
            self.start = [random.randint(0, N - 1) for _ in range(N)]
        else:
            self.start = start
    
        print("Initial State:", self.start)

    def is_safe(self, row, col):
        for i in range(col):
            if self.board[row][i] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        for i, j in zip(range(row, self.N, 1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        return True

    def print_board(self):
        if self.board==[[0] * self.N for _ in range(self.N)]:
            return "No Solution Found",time.time()-self.timing
        return self.board,time.time()-self.timing


        
    def show_board(self):
        table_container = GUI.show_table(self.board, self.N)
        if globals.outt is not None:
            globals.outt.content = table_container
            globals.pagge.update()
    
    
    def place_queen(self, row, col):
        self.board[row][col] = 1
        self.show_board()

    def remove_queen(self, row, col):
        self.board[row][col] = 0
        self.show_board()
###############################################################################################################################
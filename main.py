

########################################################--Board Class--########################################################
class Board:
    def __init__(self, N):
        self.N = N
        self.board = [[0] * N for _ in range(N)]

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

    def print_solution(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.board[i][j], end=" ")
            print()

    def place_queen(self, row, col):
        self.board[row][col] = 1

    def remove_queen(self, row, col):
        self.board[row][col] = 0
###############################################################################################################################


###############################################--Backtracking Search Algorithm--###############################################

def backtrack(board, col):
    if col >= board.N:
        return True

    for i in range(board.N):
        if board.is_safe(i, col):
            board.place_queen(i, col)

            if backtrack(board, col + 1):
                return True

            board.remove_queen(i, col)

    return False
###############################################################################################################################


def solve(N,C):
    board = Board(N)
    match C:
        case 1:
            if not backtrack(board, 0):
                print("No Solution")
        case 2:
            # if not best_First(board, 0):
            #     print("error")
            print("Not implemented yet..")
        case 3:
            # if not hill_Climbing(board, 0):
            #     print("error")
            print("Not implemented yet..")
        case 4:
            # if not cultural(board, 0):
            #     print("error")
            print("Not implemented yet..")
        case _:
            print("No Such Search Algorithm")

    board.print_solution()


###########################################################--Main--############################################################
N = int(input("\nEnter N\n"))
C =int(input("Choose Search Algorithm Number:\n1.Backtracking Search Algorithm\n2.Best-First Search\n3.Hill-Climbing Search\n4.Cultural Algorithm\n"))
solve(N,C)
###############################################################################################################################




############################################################--GUI--#############################################################



###############################################################################################################################


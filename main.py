import flet as ft
import heapq
import random
import time

########################################################--Board Class--########################################################
class Board:
    def __init__(self, N):
        self.N = N
        self.board = [[0] * N for _ in range(N)]
        self.timing=time.time()

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

    def place_queen(self, row, col):
        self.board[row][col] = 1

    def remove_queen(self, row, col):
        self.board[row][col] = 0
###############################################################################################################################



###########################################################################--Algorithms--###########################################################################

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


################################################--Best-First Search Algorithm--################################################


def heuristicBF1(state, n):
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def heuristicBF2(state, n):
    row = [0] * n
    d1 = [0] * (2*n)
    d2 = [0] * (2*n)

    for c in range(n):
        r = state[c]
        row[r] += 1
        d1[c + r] += 1
        d2[c - r + n] += 1

    conflicts = 0
    for c in range(n):
        r = state[c]
        conflicts += (row[r] - 1)
        conflicts += (d1[c + r] - 1)
        conflicts += (d2[c - r + n] - 1)

    return conflicts


def best_first(board):
    n = board.N
    start = [random.randint(0, n - 1) for _ in range(n)]
    pq = [(heuristicBF1(start, n), start)]
    visited = set()

    while pq:
        h, state = heapq.heappop(pq)

        if h == 0:
            for col in range(n):
                board.place_queen(state[col], col)
            return True
        visited.add(tuple(state))
        for i in range(n):
            for j in range(n):
                if j != state[i]:
                    new_state = state.copy()
                    new_state[i] = j
                    if tuple(new_state) not in visited:
                        heapq.heappush(pq, (heuristicBF1(new_state, n), new_state))
    return False
###############################################################################################################################









############################################################--GUI--#############################################################
#To run write flet run main.py in terminal but please make sure you installed flet by putting "pip install flet" in terminal/cmd
def main(page: ft.Page):
    page.title = "N-Queens Problem"
    page.adaptive=True
    page.appbar = ft.AppBar(
        title = ft.Text(value="N-Queens", color="green", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        center_title=True
        )
    page.window.width = 600
    page.window.height = 700
    page.auto_scroll = True
    page.scroll= "ALWAYS"
    

    def show_table(result):
        columns = [ft.DataColumn(ft.Text("")) for _ in range(int(Ntiles.value))]
        rows = []
        for row_data in result:
                cells = []
                for cell in row_data:
                    if cell == 1:
                        cells.append(ft.DataCell(ft.Icon(name=ft.Icons.PERSON_4_SHARP, color=ft.Colors.GREEN)))
                    else:
                        cells.append(ft.DataCell(ft.Text(str(" "))))
                rows.append(ft.DataRow(cells=cells))

        table = ft.DataTable(columns=columns, rows=rows, border=ft.border.all(3, ft.Colors.WHITE), border_radius=10,
            heading_row_height=0,vertical_lines=ft.border.BorderSide(3, ft.Colors.WHITE),
            horizontal_lines=ft.border.BorderSide(3, ft.Colors.WHITE),)
        return table



    def button_clicked(e):
        result, timing = solve(int(Ntiles.value), int(color_dropdown.value))
        if isinstance(result, list):
            

            
            output_container.content = show_table(result)
        else:
            output_text.value = result
            output_container.content = output_text
        output_time.value = f"Time taken: {timing:.6f} seconds"
        page.update()

    def all_Clicked(e):

        open_new(Ntiles.value,1)
        page.update()


    

    def open_new(n,algo):
        result, timing = solve(int(n), algo)

        x=""
        match algo:
            case 1: x="Backtracking Search"
            case 2: x="Best-First Search"
            case 3: x="Hill-Climbing Search"
            case 4: x="Cultural Algorithm"

        if isinstance(result, list):
            table = show_table(result)
            content=ft.Column(
                    [
                        ft.Text(value=x, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        table,
                        ft.Text(f"Time taken: {timing:.6f} seconds")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            
        else:
            content=ft.Column(
                    [
                        ft.Text(value=x, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text(result),
                        ft.Text(f"Time taken: {timing:.6f} seconds")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )




        new_page=ft.AlertDialog(
        modal=True,
        title = "N-Queens Solution",
        content=content,
        alignment=ft.alignment.center,
        actions=[],
        actions_alignment=ft.MainAxisAlignment.END,
        )
        def next(e):
            page.close(new_page)
            if algo<4:
                open_new(n, algo+1)
        
        new_page.actions=[ft.ElevatedButton("Next", on_click=next, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)]

        page.open(new_page)
            

    
    output_text = ft.Text()
    output_time = ft.Text()
    output_container = ft.Container(content=output_text, alignment=ft.alignment.center,)
    submit_btn = ft.ElevatedButton(text="Solve", on_click=button_clicked, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
    color_dropdown = ft.Dropdown(
        text_align=ft.TextAlign.CENTER,
        hint_text="Select Search Algorithm",
        options=[
            ft.dropdown.Option(1,"Backtracking Search"),
            ft.dropdown.Option(2,"Best-First Search"),
            ft.dropdown.Option(3,"Hill-Climbing Search"),
            ft.dropdown.Option(4,"Cultural Algorithm"),
        ],
    )

    Ntiles = ft.TextField(hint_text="Enter Number of tiles", width=200, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    all_btn = ft.ElevatedButton(text="All?", on_click=all_Clicked, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)

    page.add(
        ft.Container(
            content=ft.SafeArea(
                ft.Column(
                    [
                       ft.Row([Ntiles, all_btn], alignment=ft.MainAxisAlignment.CENTER ),
                        color_dropdown,
                        submit_btn,
                        output_container,
                        output_time
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ),
            expand=True,
            alignment=ft.alignment.center,
            # padding=ft.padding.only(top=-48)
        ),

    )
    



###############################################################################################################################

###########################################################--Main--############################################################

def solve(N,C):
    board = Board(N)
    match C:
        case 1:
            backtrack(board, 0)
        case 2:
            best_first(board)
        case 3:
            # if not hill_Climbing(board, 0):
            #     print("error")
            return("Not implemented yet..") ,0
        case 4:
            # if not cultural(board, 0):
            #     print("error")
            return("Not implemented yet.."),0
        case _:
            return("No Such Search Algorithm"),0
    # return print_board(board)
    return board.print_board()

ft.app(main)

# N = int(input("\nEnter N\n"))
# C =int(input("Choose Search Algorithm Number:\n1.Backtracking Search Algorithm\n2.Best-First Search\n3.Hill-Climbing Search\n4.Cultural Algorithm\n"))
# solve(N,C)

###############################################################################################################################
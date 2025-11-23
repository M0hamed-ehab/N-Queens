import flet as ft
import heapq
import random
import time

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

def backtrack(board, col=0):
    if col >= board.N:
        return True

    start = board.start[col]
    for offset in range(board.N):
        i = (start + offset) % board.N
        if board.is_safe(i, col):
            board.place_queen(i, col)

            if backtrack(board, col + 1):
                return True

            board.remove_queen(i, col)

    return False
###############################################################################################################################


################################################--Best-First Search Algorithm--################################################


class Heuristics:
    
    @staticmethod
    def heuristic1(state, n):
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    @staticmethod
    def heuristic2(state, n):
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
    
    current = heuristic1

    @staticmethod
    def set_heuristic(num):
        if num == 1:
            Heuristics.current = Heuristics.heuristic1
            print("Heuristic set to heuristic1")
        elif num == 2:
            Heuristics.current = Heuristics.heuristic2
            print("Heuristic set to heuristic2")
        else:
            Heuristics.current = Heuristics.heuristic1
            print("Heuristic set to default heuristic1")





def best_first(board):
    n = board.N
    start = board.start.copy()
    heuristic = Heuristics.current
    pq = [(heuristic(start, n), start)]
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
                        heapq.heappush(pq, (heuristic(new_state, n), new_state))
    return False

    

###############################################################################################################################





###############################################--Hill-Climbing Search Algorithm--###############################################

def hill_climbing(board, maxrestarts=50):
    n = board.N
    heuristic = Heuristics.current

    def get_neighbors(state):
        neighbors = []
        for i in range(n):
            for j in range(n):
                if j != state[i]:
                    new_state = state.copy()
                    new_state[i] = j
                    neighbors.append(new_state)
        return neighbors

    for _ in range(maxrestarts):
        if _ == 0:
            current = board.start.copy()
        else:
            current = [random.randint(0, n - 1) for _ in range(n)]

        current_h = heuristic(current, n)
        while True:
            neighbors = get_neighbors(current)
            next_state = min(neighbors, key=lambda s: heuristic(s, n))
            next_h = heuristic(next_state, n)
            if next_h >= current_h:
                break
            current, current_h = next_state, next_h
        if current_h == 0:
            for col in range(n):
                board.place_queen(current[col], col)
            return True
    return False

###############################################################################################################################







##################################################--Culture Search Algorithm--##################################################

def cultural(board, population_size=110, generations=700):
    heuristic = Heuristics.current

    def fitness(state):
        return 1 / (1 + heuristic(state, n))

    n = board.N
    population =([board.start.copy()] + [[random.randint(0, n - 1) for _ in range(n)]for _ in range(population_size - 1)] )

    belief = board.start.copy()

    for gen in range(generations):
        population.sort(key=lambda s: heuristic(s, n))
        best = population[0]
        if heuristic(best, n) == 0:
            for col in range(n):
                board.place_queen(best[col], col)
            return True

        top_half = population[:population_size // 2]
        for i in range(n):
            belief[i] = random.choice([s[i] for s in top_half])

        new_pop = []
        for _ in range(population_size):
            parent = random.choice(top_half)
            child = parent.copy()
            idx = random.randint(0, n - 1)
            child[idx] = belief[idx] if random.random() < 0.5 else random.randint(0, n - 1)
            new_pop.append(child)
        population = new_pop
    return False

############################################################--GUI--#############################################################
#To run write python main.py in terminal but please make sure you installed flet by putting "pip install flet" in terminal/cmd
def main(page: ft.Page):
    page.title = "N-Queens Problem"
    page.adaptive=True
    
    def handle_dismissal(e):
        print(f"Drawer dismissed!")

    def handle_change(e):
        print(f"Selected Index changed: {e.control.selected_index}")
        page.close(drawer)    
        
    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        tile_padding=ft.padding.all(10),
        controls=[
            ft.Container(height=30),
            ft.Text("Select Heuristic", size=20, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREEN),
            ft.Container(                 
                content=ft.RadioGroup(
                            content=ft.Row(
                            [
                            ft.Radio(value="1", label="1",adaptive=True,expand=True),
                            ft.Radio(value="2", label="2",adaptive=True,expand=True),

                            ], alignment=ft.MainAxisAlignment.CENTER, expand=True
                            ), on_change=lambda e: Heuristics.set_heuristic(1 if e.control.value=="1" else 2), value="1"
                            ), 
                        padding=ft.padding.all(10)
                    ),
            ft.Divider(thickness=2),
            ft.Text("Select Heuristic", size=20, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREEN),

            
           
            
        ],
    )
    
    
    
    
    
    page.appbar = ft.AppBar(
        title = ft.Text(value="N-Queens", color="green", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        center_title=True, actions=[ft.IconButton(ft.Icons.SETTINGS_ROUNDED,on_click=lambda e: page.open(drawer)),],
        )
    # page.window.width = 600
    # page.window.height = 700
    page.auto_scroll = True
    page.scroll= "ALWAYS"

    def show_green(r, c, result):
        n = int(Ntiles.value)
        green = set()

        for i in range(n):
            green.add((r, i)) 
            green.add((i, c)) 

        for i in range(n):
            for j in range(n):
                if abs(r - i) == abs(c - j):
                    green.add((i, j))


        columns = [ft.DataColumn(ft.Text("")) for _ in range(n)]
        rows = []
        for i in range(n):
            cells = []
            for j in range(n):

                if (i, j) in green:
                    if result[i][j] == 1:
                        cells.append(ft.DataCell(ft.Icon(name=ft.Icons.PERSON_4_SHARP, color=ft.Colors.LIGHT_GREEN), on_tap=lambda e, r=i, c=j: show_green(r, c, result)))
                    else:
                        cells.append(ft.DataCell(ft.Icon(name=ft.Icons.CLOSE_ROUNDED, color=ft.Colors.LIGHT_GREEN)))
                else:
                    if result[i][j] == 1:
                        cells.append(ft.DataCell(ft.Icon(name=ft.Icons.PERSON_4_SHARP, color=ft.Colors.GREEN), on_tap=lambda e, r=i, c=j: show_green(r, c, result)))
                    else:
                        cells.append(ft.DataCell(ft.Text(str(" "))))

            rows.append(ft.DataRow(cells=cells))

        table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(3, ft.Colors.WHITE),
            border_radius=10,
            heading_row_height=0,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.WHITE),
            horizontal_lines=ft.border.BorderSide(3, ft.Colors.WHITE),
            expand=True
        )
        table_container = ft.Container(
            content=ft.Row(
                controls=[table],
                scroll=ft.ScrollMode.ALWAYS,
            ),
            expand=True,
            padding=10,
        )
        output_container.content = table_container
        page.update()


    def show_table(result,comp=False):
        columns = [ft.DataColumn(ft.Text("")) for _ in range(int(Ntiles.value))]
        rows = []
        

        
        for r, row_data in enumerate(result):
            cells = []
            for c, cell in enumerate(row_data):
                if cell == 1:
                    if comp:
                        cells.append(ft.DataCell(ft.Icon(name=ft.Icons.PERSON_4_SHARP, color=ft.Colors.GREEN)))
                    else:
                        cells.append(ft.DataCell(ft.Icon(name=ft.Icons.PERSON_4_SHARP, color=ft.Colors.GREEN,), on_tap=lambda e, r=r, c=c: show_green(r, c, result)))
                else:
                    cells.append(ft.DataCell(ft.Text(str(" "))))
            rows.append(ft.DataRow(cells=cells))

        table = ft.DataTable(columns=columns, rows=rows, border=ft.border.all(3, ft.Colors.WHITE), border_radius=10, heading_row_height=0,
            vertical_lines=ft.border.BorderSide(3, ft.Colors.WHITE), horizontal_lines=ft.border.BorderSide(3, ft.Colors.WHITE),)
        
        table_container = ft.Container(
            content=ft.Row(
                controls=[table],
                scroll=ft.ScrollMode.ALWAYS, 
            ),
            expand=True,
            padding=10,
        )
        return table_container

    def validation():
        if not Ntiles.value.isdigit() or int(Ntiles.value)<=0:
            output_text.value = "Please enter a valid positive integer for number of tiles."
            output_container.content = output_text
            output_time.value = ""
            page.update()
            return
        if color_dropdown.value is None:
            output_text.value = "Please select a search algorithm."
            output_container.content = output_text
            output_time.value = ""
            page.update()
            return



    def button_clicked(e):
        validation()
        result, timing = solve(int(Ntiles.value), int(color_dropdown.value))
        if isinstance(result, list):
            

            
            output_container.content = show_table(result)
        else:
            output_text.value = result
            output_container.content = output_text
        output_time.value = f"Time taken: {timing:.6f} seconds"
        page.update()

    def all_Clicked(e):
        validation()
        page.all_results=[]
        start=[random.randint(0, int(Ntiles.value) - 1) for _ in range(int(Ntiles.value))]
        solve_all(int(Ntiles.value), start)
        page.update()

    def show_comp():
        columns=[
            ft.DataColumn(ft.Text("Algorithm")),
            ft.DataColumn(ft.Text("Time Taken (seconds)")),
        ]
        rows=[]
        for name,t, timing in page.all_results:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(f"{timing:.6f}"))
                    ]
                )
            )
        table=ft.DataTable(columns=columns, rows=rows, border=ft.border.all(1, ft.Colors.WHITE), border_radius=10)

        content=ft.Column(
            [
                ft.Text("Comparison of Algorithms", weight=ft.FontWeight.BOLD, size=18, text_align=ft.TextAlign.CENTER),
                table,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        compall=ft.AlertDialog(
            modal=True,
            title="N-Queens Comparison",
            content=content,
            alignment=ft.alignment.center,
            actions=[
                ft.ElevatedButton("Close",bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE,on_click=lambda e: page.close(compall))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(compall)


    def solve_all(n, start):
        page.all_results=[]
        
        for al in range(1,5):
            x=""
            match al:
                case 1: x="Backtracking Search"
                case 2: x="Best-First Search"
                case 3: x="Hill-Climbing Search"
                case 4: x="Cultural Algorithm"
                
            result, timing=solve(int(n), al, start)
            page.all_results.append((x,result,timing))

            open_new(int(n), 1, start)
     

    def open_new(n, algo, start):
        
        
        if algo> 4:
            show_comp()
            return
        
        x,result,timing=page.all_results[algo-1]


        if isinstance(result, list):
            table = show_table(result,comp=True)
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
        scrollable=True,
        )

        def next(e):
            page.close(new_page)
            open_new(n, algo+1, start)
                    

        new_page.actions=[ft.ElevatedButton("Next", on_click=next, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)]

        page.open(new_page)
            

    
    output_text = ft.Text()
    output_time = ft.Text()
    output_container = ft.Container(content=output_text, alignment=ft.alignment.center, expand=True)
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
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS
                )
            ),
            expand=True,
            alignment=ft.alignment.center,
            
            # padding=ft.padding.only(top=-48)
        ),

        )
    



###############################################################################################################################

###########################################################--Main--############################################################

def solve(N,C,start= -1):
    board = Board(N, start)
    match C:
        case 1:
            backtrack(board)
        case 2:
            best_first(board)
        case 3:
            hill_climbing(board)
        case 4:
            cultural(board)
        case _:
            return("No Such Search Algorithm"),0
    # return print_board(board)
    return board.print_board()

ft.app(main)

# N = int(input("\nEnter N\n"))
# C =int(input("Choose Search Algorithm Number:\n1.Backtracking Search Algorithm\n2.Best-First Search\n3.Hill-Climbing Search\n4.Cultural Algorithm\n"))
# solve(N,C)

###############################################################################################################################

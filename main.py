import flet as ft


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

    def print_board(self):
        board=""
        for i in range(self.N):
            for j in range(self.N):
                board+=str(self.board[i][j])+" "
            board+="\n"
        return board

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
                return("No Solution")
        case 2:
            # if not best_First(board, 0):
            #     print("error")
            return("Not implemented yet..")
        case 3:
            # if not hill_Climbing(board, 0):
            #     print("error")
            return("Not implemented yet..")
        case 4:
            # if not cultural(board, 0):
            #     print("error")
            return("Not implemented yet..")
        case _:
            return("No Such Search Algorithm")
    # return print_board(board)
    return board.board







############################################################--GUI--#############################################################
#To run write flet run main.py in terminal but please make sure you installed flet by putting "pip install flet" in terminal/cmd
def main(page: ft.Page):
    page.title = "N-Queens Problem"
    page.adaptive=True
    page.appbar = ft.AppBar(
        title = ft.Text(value="N-Queens", color="green", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        center_title=True
        )
    
    

    def button_clicked(e):
        result = solve(int(Ntiles.value), int(color_dropdown.value))
        if isinstance(result, list):
            

            columns = [ft.DataColumn(ft.Text("")) for _ in range(int(Ntiles.value))]
            rows = []
            for row_data in result:
                cells = [ft.DataCell(ft.Text(str(cell))) for cell in row_data]
                rows.append(ft.DataRow(cells=cells))

            table = ft.DataTable(columns=columns, rows=rows, border=ft.border.all(1, ft.Colors.BLACK), heading_row_height=0)
            output_container.content = table
        else:
            output_text.value = result
            output_container.content = output_text
        page.update()
    
    output_text = ft.Text()
    output_container = ft.Container(content=output_text, height=400, alignment=ft.alignment.center)
    submit_btn = ft.ElevatedButton(text="Solve", on_click=button_clicked, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
    color_dropdown = ft.Dropdown(
        text_align=ft.TextAlign.CENTER,
        hint_text="Select Search Algorithm",
        options=[
            ft.dropdown.Option(1,"Backtracking Search Algorithm"),
            ft.dropdown.Option(2,"Best-First Search"),
            ft.dropdown.Option(3,"Hill-Climbing Search"),
            ft.dropdown.Option(4,"Cultural Algorithm"),
        ],
    )

    Ntiles = ft.TextField(hint_text="Enter Number of tiles", width=200, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    page.add(
        ft.Container(
            content=ft.SafeArea(
                ft.Column(
                    [
                        Ntiles,
                        color_dropdown,
                        submit_btn,
                        output_container
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ),
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=-50)
        ),

    )



###############################################################################################################################

###########################################################--Main--############################################################
ft.app(main)

# N = int(input("\nEnter N\n"))
# C =int(input("Choose Search Algorithm Number:\n1.Backtracking Search Algorithm\n2.Best-First Search\n3.Hill-Climbing Search\n4.Cultural Algorithm\n"))
# solve(N,C)

###############################################################################################################################
import flet as ft
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flet.matplotlib_chart import MatplotlibChart
from classes.board import Board
from classes.heuristics import Heuristics
from classes.searches import SA
import globals

matplotlib.use("svg")

def plot_cultural_progress(history_best, title="Cultural Algo Progress"):
    generations = len(history_best)
    gens = list(range(1, generations + 1))
    best = np.array(history_best)

    mid = generations // 2
    start_val = best[0]
    mid_val = best[mid - 1]
    end_val = best[-1]

    progress1 = start_val - mid_val
    progress2 = mid_val - end_val

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(gens, best, linewidth=2)

    ax.set_xlabel("Time (Number of Generations)")
    ax.set_ylabel("Best Fitness in Population")
    ax.set_title(title)
    ax.grid(alpha=0.3)

    ax.axvline(mid, color='gray', linestyle='--', alpha=0.6)

    ax.annotate(f"Progress in 1st half = {progress1:.2f}",
                xy=(mid/2, (start_val + mid_val)/2),
                xytext=(mid/2, max(best)*0.8),
                arrowprops=dict(arrowstyle="->", color="red"),
                color="red")

    ax.annotate(f"Progress in 2nd half = {progress2:.2f}",
                xy=(mid + (generations-mid)/2, (mid_val + end_val)/2),
                xytext=(mid + (generations-mid)/3, max(best)*0.5),
                arrowprops=dict(arrowstyle="->", color="red"),
                color="red")

    plt.tight_layout()
    return fig

def show_table(result, n, comp=False):
    columns = [ft.DataColumn(ft.Text("")) for _ in range(n)]
    rows = []

    for r, row_data in enumerate(result):
        cells = []
        for c, cell in enumerate(row_data):
            if cell == 1:
                if comp:
                    cells.append(ft.DataCell(ft.Image(src="icons/4G.png",fit=ft.ImageFit.CONTAIN, width=24,height=24)))
                else:
                    cells.append(ft.DataCell(ft.Image(src="icons/4G.png",fit=ft.ImageFit.CONTAIN, width=24,height=24), on_tap=lambda e, r=r, c=c: show_green(r, c, result, n)))
            else:
                cells.append(ft.DataCell(ft.Image(src="icons/blank.png",fit=ft.ImageFit.CONTAIN, width=24,height=24)))
        rows.append(ft.DataRow(cells=cells))

    table = ft.DataTable(columns=columns, rows=rows, border=ft.border.all(3, ft.Colors.INVERSE_SURFACE), border_radius=10, heading_row_height=0,
        vertical_lines=ft.border.BorderSide(3, ft.Colors.INVERSE_SURFACE), horizontal_lines=ft.border.BorderSide(3, ft.Colors.INVERSE_SURFACE),)

    table_container = ft.Container(
        content=ft.Row(
            controls=[table],
            scroll=ft.ScrollMode.ALWAYS,
        ),
        expand=True,
        padding=10,
    )
    return table_container

def show_green(r, c, result, n):
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
                    cells.append(ft.DataCell(ft.Image(src="icons/4LG.png",fit=ft.ImageFit.CONTAIN, width=24,height=24), on_tap=lambda e, r=i, c=j: show_green(r, c, result, n)))
                else:
                    cells.append(ft.DataCell(ft.Icon(name=ft.Icons.CLOSE_ROUNDED, color=ft.Colors.LIGHT_GREEN)))
            else:
                if result[i][j] == 1:
                    cells.append(ft.DataCell(ft.Image(src="icons/4G.png",fit=ft.ImageFit.CONTAIN, width=24,height=24), on_tap=lambda e, r=i, c=j: show_green(r, c, result, n)))
                else:
                    cells.append(ft.DataCell(ft.Image(src="icons/blank.png",fit=ft.ImageFit.CONTAIN, width=24,height=24)))
        rows.append(ft.DataRow(cells=cells))

    table = ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(3, ft.Colors.INVERSE_SURFACE),
        border_radius=10,
        heading_row_height=0,
        vertical_lines=ft.border.BorderSide(3, ft.Colors.INVERSE_SURFACE),
        horizontal_lines=ft.border.BorderSide(3, ft.Colors.INVERSE_SURFACE),
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
    globals.outt.content = table_container
    globals.pagge.update()


############################################################--GUI--#############################################################
#To run write python main.py in terminal but please make sure you installed flet by putting "pip install flet" in terminal/cmd
def main(page: ft.Page):
    page.title = "N-Queens Problem"
    page.adaptive=True
    
    globals.pagge = page

    
    def handle_dismissal(e):
        print(f"Drawer dismissed!")

    def handle_change(e):
        print(f"Selected Index changed: {e.control.selected_index}")
        page.close(drawer)
    
    
    
    def set_MRes(e):
        print(MRes.value)
        if MRes.value!='':
            globals.maxrestarts = int(MRes.value)


    def set_Popp(e):
        print(Popp.value)
        if Popp.value!='':
            globals.population_size = int(Popp.value)

    def set_Genn(e):
        print(Genn.value)
        if Genn.value!='':
            globals.generations = int(Genn.value)

    def set_Rif(e):
        globals.refresh_if_stuck = e.control.value
        print(globals.refresh_if_stuck)
    
    
        
    
    MRes=ft.TextField(hint_text="Max Restarts: Default 50", text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    MRB=ft.ElevatedButton(text="Set", on_click=set_MRes, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE,)
    
    Popp=ft.TextField(hint_text="Population Size: Default 110", text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    PoppB=ft.ElevatedButton(text="Set", on_click=set_Popp, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE,)
    
    Genn=ft.TextField(hint_text="Generations: Default 700", text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    GennB=ft.ElevatedButton(text="Set", on_click=set_Genn, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE,)

    Rif_checkbox=ft.Checkbox(label="Refresh if Stuck", value=False, on_change=set_Rif, active_color=ft.Colors.GREEN)
    
    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        tile_padding=ft.padding.all(10),
        controls=[
            ft.Container(height=30),
            ft.Text("Select Heuristic", size=20, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREEN),
            ft.Container(                 
                content=ft.RadioGroup(
                            content=ft.Column(
                            [
                            ft.Radio(value="1", label="Number of attacking pairs (optimized)",adaptive=True,expand=True),
                            ft.Radio(value="2", label="Number of queens being attacked",adaptive=True,expand=True),
                            ft.Radio(value="3", label="Number of attacking pairs",adaptive=True,expand=True),

                            ], alignment=ft.MainAxisAlignment.CENTER, expand=True
                            ), on_change=lambda e: Heuristics.set_heuristic(1 if e.control.value=="1" else 2 if e.control.value=="2" else 3), value="1"
                            ), 
                        padding=ft.padding.all(10)
                    ),
            ft.Divider(thickness=2),
            ft.Text("Hill-Climbing", size=20, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREEN),
            ft.Container( 
                content=ft.Column(
                [MRes, ft.Container(height=10),
                 MRB]
                ) , padding=ft.padding.all(10), alignment=ft.alignment.center),
            ft.Divider(thickness=2),
            ft.Text("Culture", size=20, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREEN),
            ft.Container(
                content=ft.Column(
                [Popp, ft.Container(height=10),
                 PoppB,ft.Container(height=10),Genn,
                 ft.Row([ ft.Container(height=10),GennB,ft.Container(height=10), Rif_checkbox])]
                ) , padding=ft.padding.all(10), alignment=ft.alignment.center),

            

            

           
            
            
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
        result, timing = SA.solve(int(Ntiles.value), int(color_dropdown.value), page=page, container=output_container, maxrestarts=globals.maxrestarts, population_size=globals.population_size, generations=globals.generations,refresh_if_stuck=globals.refresh_if_stuck)
        if isinstance(result, list):




            output_container.content = show_table(result, int(Ntiles.value))
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
        table=ft.DataTable(columns=columns, rows=rows, border=ft.border.all(1, ft.Colors.INVERSE_SURFACE), border_radius=10)

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
                ft.ElevatedButton("Show Plot", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, on_click=lambda e: show_plot()),
                ft.ElevatedButton("Close",bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE,on_click=lambda e: page.close(compall))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(compall)
    
    
    def show_plot():
        names = []
        timings = []

        for name, t, timing in page.all_results:
            names.append(name)
            timings.append(timing)
        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(names, timings)
        ax.set_xlabel("Algorithm")
        ax.set_ylabel("Time Taken (seconds)")
        ax.set_title("Algorithm Performance Comparison")

        chart = MatplotlibChart(fig, expand=True)
        
        if globals.history_best:
            actions=[
                ft.ElevatedButton("Show Plot", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE, on_click=lambda e: show_Cplot()),

                ft.ElevatedButton( "Close",bgcolor=ft.Colors.GREEN,color=ft.Colors.WHITE,on_click=lambda e: page.close(dialog))
            ]
        else:
            actions=[
                ft.ElevatedButton( "Close",bgcolor=ft.Colors.GREEN,color=ft.Colors.WHITE,on_click=lambda e: page.close(dialog))
            ]
            

        dialog = ft.AlertDialog(
            modal=True,
            title="Performance Plot",
            content=ft.Container(chart, width=600, height=400),
            
            
                
            
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
        )
        

        page.open(dialog)
        
        
    show_cplot_btn = ft.ElevatedButton(
    text="Show Plot",
    visible=False,
    on_click=lambda e: show_Cplot(),
    bgcolor=ft.Colors.BLUE,
    color=ft.Colors.WHITE
    )

        
    def show_Cplot():
            
        fig = plot_cultural_progress(globals.history_best)
        chart = MatplotlibChart(fig, expand=True)
        dialog = ft.AlertDialog( modal=True, title="Cultural Algorithm Progress", content=ft.Container(chart, width=600, height=400),
                actions=[
                        ft.ElevatedButton("Close", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, on_click=lambda e: page.close(dialog))
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            
        page.open(dialog)
        


    def solve_all(n, start):
        page.all_results=[]

        for al in range(1,5):
            x=""
            match al:
                case 1: x="Backtracking Search"
                case 2: x="Best-First Search"
                case 3: x="Hill-Climbing Search"
                case 4: x="Cultural Algorithm"

            result, timing=SA.solve(int(n), al, start)
            page.all_results.append((x,result,timing))

        open_new(int(n), 1, start)
     

    def open_new(n, algo, start):
        
        
        if algo> 4:
            show_comp()
            return
        
        x,result,timing=page.all_results[algo-1]


        if isinstance(result, list):
            table = show_table(result, n, comp=True)
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
        
        on_change= lambda e: (setattr(show_cplot_btn, 'visible', e.control.value=="4"), page.update())
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
                        ft.Row(
                        [submit_btn, show_cplot_btn],
                        alignment=ft.MainAxisAlignment.CENTER
                        ),

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
    globals.outt = output_container


###############################################################################################################################

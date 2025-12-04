import heapq
import random
import time
from classes.heuristics import Heuristics
from classes.board import Board
import globals

class SA:
    @staticmethod
    def backtrack(board, col=0):
        if col >= board.N:
            return True

        # start = board.start[col]
        # for offset in range(board.N):
        for i in range(board.N):
            # i = (start + offset) % board.N
            if board.is_safe(i, col):
                board.place_queen(i, col)

                if SA.backtrack(board, col + 1):
                    return True

                board.remove_queen(i, col)

        return False

    @staticmethod
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

    @staticmethod
    def hill_climbing(board, maxrestarts=50):
        n = board.N
        heuristic = Heuristics.current
        print(f"\nMax Restarts={maxrestarts}\n")
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

    @staticmethod
    def cultural(board, population_size=110, generations=700, refresh_if_stuck=False):
        heuristic = Heuristics.current
        print(f"\nPopulation Size={population_size}\n")
        print(f"\nGenerations={generations}\n")
        n = board.N

        population = ([board.start.copy()] + [[random.randint(0, n - 1) for _ in range(n)] for _ in range(population_size - 1)])

        belief = board.start.copy()

        # Track the best heuristic value and stagnation count
        best_heuristic = heuristic(board.start, n)
        stagnation_count = 0

        globals.history_best = []  

        for gen in range(generations):
            population.sort(key=lambda s: heuristic(s, n))
            best = population[0]
            current_best_heuristic = heuristic(best, n)
            globals.history_best.append(current_best_heuristic)  # Track best fitness
            if current_best_heuristic == 0:
                for col in range(n):
                    board.place_queen(best[col], col)
                return True

            # Check for improvement
            if current_best_heuristic < best_heuristic:
                best_heuristic = current_best_heuristic
                stagnation_count = 0
            else:
                stagnation_count += 1

            # If refresh_if_stuck is True and stagnation detected, refresh population
            if refresh_if_stuck and stagnation_count >= 10:
                population = ([board.start.copy()] + [[random.randint(0, n - 1) for _ in range(n)] for _ in range(population_size - 1)])
                belief = population[0].copy()  # Reset belief to the new best (initially board.start)
                stagnation_count = 0
                best_heuristic = heuristic(population[0], n)
                continue  # Skip the rest of the generation logic and proceed to the next generation

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
    @staticmethod
    def solve(N, C, start=-1, maxrestarts=50, population_size=110, generations=700, refresh_if_stuck=False, page=None, container=None):
        import globals
        if page is not None:
            globals.pagge = page
        if container is not None:
            globals.outt = container
        board = Board(N, start)
        match C:
            case 1:
                SA.backtrack(board)
            case 2:
                SA.best_first(board)
            case 3:
                SA.hill_climbing(board, maxrestarts)
            case 4:
                SA.cultural(board, population_size, generations, refresh_if_stuck)
            case _:
                return ("No Such Search Algorithm"), 0
        return board.print_board()

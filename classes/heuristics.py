########################################################--Heuristics Class--########################################################
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


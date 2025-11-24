########################################################--Heuristics Class--########################################################
class Heuristics:
    
    @staticmethod
    def heuristic1(state, n):
        # Counts the number of pairs of queens that are attacking each other
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    @staticmethod
    def heuristic2(state, n):
        # Counts the number of  queens that are attacking each other
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
    
    @staticmethod
    def heuristic3(state, n):
        # Counts the number of attacking pairs by checking each queen against all others
        conflicts = 0
        for c in range(n):
            r= state[c]
            for c2 in range(n):
                if c==c2:
                    continue
                r2= state[c2]
                if r==r2:
                    conflicts += 1
                if abs(r - r2) == abs(c - c2):
                    conflicts += 1
        return conflicts // 2
    
    current = heuristic1

    @staticmethod
    def set_heuristic(num):
        if num == 1:
            Heuristics.current = Heuristics.heuristic1
            print("Heuristic set to heuristic1")
        elif num == 2:
            Heuristics.current = Heuristics.heuristic2
            print("Heuristic set to heuristic2")
        elif num == 3:
            Heuristics.current = Heuristics.heuristic3
            print("Heuristic set to heuristic3")
        else:
            Heuristics.current = Heuristics.heuristic1
            print("Heuristic set to default heuristic1")


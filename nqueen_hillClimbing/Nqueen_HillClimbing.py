# Yiqing Li
# 2023/03/30
# =============================
import random
import copy
import numpy as np

N = int(input("How many queens?"))
Neighbor_size = 6
max_iter = 200
k = 100

class NQueen:
    def __init__(self,queen_num=N, queen_loc=None,max_iter=max_iter,k=k):
        self.queen_num = queen_num
        self.queen_loc = queen_loc

        self.state = -500
        self.goal = 0
        self.max_iter = max_iter
        self.k = k

    def RandomState(self):
        open_columns = list(range(self.queen_num))
        # no repeat in columns
        queen_positions = [(open_columns.pop(random.randrange(len(open_columns))), random.randrange(self.queen_num)) for _ in
                           range(self.queen_num)]
        #print("queens:",queen_positions)
        return queen_positions

    def CalState(self,input_loc):
        # Implement a method for enumerating states in a defined environment (purpose function)
        state = 0
        for loc1 in input_loc:
            for loc2 in input_loc:
                if (loc2 != loc1) and (loc1[1] == loc2[1]):
                    state -= 1
                if (loc2[1]-loc2[0] == loc1[1]-loc1[0]) or (loc2[1]+loc2[0] == loc1[1]+loc1[0]):
                    state -= 1
            state = state//2
        return state


    def RandomNeighbor(self):
        # all possible neighbors
        neighbor = []
        queen_locations = copy.copy(self.queen_loc)
        for index,q in enumerate(queen_locations):
            new_locations = []
            for r in range(self.queen_num):
                if r != q[1]:
                    new_locations.append((q[0],r))
            for new_loc in new_locations:
                if abs(new_loc[1]- queen_locations[index][1]) <= Neighbor_size: # range of local search
                    new_queens = copy.copy(self.queen_loc)
                    new_queens[index] = new_loc
                    neighbor.append(new_queens)
        return neighbor
        #print(neighbor)

    def visualize(self,x):
        qmap = np.array(np.zeros((self.queen_num, self.queen_num), dtype = str))
        qmap[:] = "."
        for loc in x:
            qmap[loc[0]][loc[1]] = "Q"
        print(qmap)

    def HillClimbing(self):
        # Steepest ascent Hill-climbing
        # restart and sideways move
        trytimes = 0
        best_result = []
        best_state = -1000
        while self.state != self.goal and trytimes < self.queen_num*10: # random restart
            self.queen_loc = self.RandomState()
            start_loc = copy.copy(self.queen_loc)
            self.state = self.CalState(self.queen_loc)
            start_state = copy.copy(self.state)
            i = 0
            while self.state < self.goal and i < self.max_iter: # goal is zero
                y = random.choice(self.RandomNeighbor())  # random_neighbor(x)
                y_state= self.CalState(y)
                #print(y_state)
                for t in range(1,k+1):
                    z = random.choice(self.RandomNeighbor())
                    z_state = self.CalState(z)
                    if z_state > y_state:
                        #print("z is better than y")
                        y = z
                        y_state = z_state
                if y_state > self.state:
                    self.queen_loc = y
                    self.state = y_state
                i = i + 1
            if self.state > best_state:
                best_result = copy.copy(self.queen_loc)
                best_state = copy.copy(self.state)

            trytimes += 1
        print("start queens:", start_loc)
        print("start state:",start_state)
        self.visualize(start_loc)
        print("best_result:",best_result)
        print("best_state:",best_state)
        self.visualize(best_result)
        print("restart times:",trytimes)
        #return self.queen_loc

    def run(self):
        self.HillClimbing()


if __name__ == '__main__':
    MyQueen = NQueen(N,max_iter)
    MyQueen.run()
# Yiqing Li
# 2023/03/11
# =============================
import random
import re
import turtle
import copy
import os

def print_maze(maze,width=3):
    for l in maze:
        for char in l:
            print(char.center(width),end='')
        print()

class Maze(object):
    def __init__(self,filepath,alg):
        self.start = (0,0)
        self.end = (0,0)
        self.pos = (0,0)
        self.prev = {}
        self.maze = []
        self.mazepath = []
        self.goal = []
        self.filepath = filepath
        self.rows = 0
        self.columns = 0
        self.open = []
        self.closed = []
        self.alg = alg

        #movement
        self.dirs = [(0,1),(1,0),(0,-1),(-1,0)] #directions while moving

        #visualize maze
        self.boxwidth=10
        self.screenwidth=0
        self.screenlength=0
        self.t = turtle.Turtle()
        self.wn = 0

    def read_maze(self):
        with open(self.filepath, "r") as f:
            data = f.read().split("\n")
            data.pop()
        self.start = tuple(map(int, re.findall(r'\d+', data[-2])))
        self.pos = copy.copy(self.start) #must use deepcopy
        self.end = tuple(map(int, re.findall(r'\d+', data[-1])))
        self.maze = data[:-2]
        self.rows = len(self.maze)
        self.columns = len(self.maze[0])
        self.screenwidth = self.rows*self.boxwidth
        self.screenlength = self.columns*self.boxwidth
        self.wn = turtle.setup(width = 1.0, height = 1.0)
        for l in self.maze:
            self.mazepath.append(list(l))
        self.mazepath[self.pos[1]][self.pos[0]]='1'

    def drawMaze(self):
        turtle.tracer(False)
        for y in range(self.rows):
            for x in range(self.columns):
                if self.maze[y][x]=='X':
                    self.drawBox(x*self.boxwidth+self.boxwidth/2,-y*self.boxwidth+self.boxwidth/2,"black")
        self.drawBox(self.start[0]*self.boxwidth+self.boxwidth / 2,-self.start[1]*self.boxwidth+self.boxwidth / 2,"red")
        self.drawBox(self.end[0]*self.boxwidth + self.boxwidth / 2, -self.end[1]*self.boxwidth + self.boxwidth / 2, "blue")

    def drawPath(self):
        #turtle.tracer(True)
        #self.t.speed(0)
        if self.mazepath[self.pos[1]][self.pos[0]] == "1":
            self.drawBox(self.pos[0] * self.boxwidth + self.boxwidth / 2,
                         -self.pos[1] * self.boxwidth + self.boxwidth / 2, "green")
        elif self.mazepath[self.pos[1]][self.pos[0]] == "2":
            self.drawBox(self.pos[0] * self.boxwidth + self.boxwidth / 2,
                         -self.pos[1] * self.boxwidth + self.boxwidth / 2, "red")
        elif self.mazepath[self.pos[1]][self.pos[0]] == "3":
            self.drawBox(self.pos[0] * self.boxwidth + self.boxwidth / 2,
                         -self.pos[1] * self.boxwidth + self.boxwidth / 2, "yellow")

    def drawBox(self,x,y,color):
        self.t.up()
        self.t.goto(x-300,y+400)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(self.boxwidth)
            self.t.right(90)
        self.t.end_fill()

    def initial(self):
        # initial open
        self.closed = [self.pos]
        self.mazepath[self.start[1]][self.start[0]] = '1'
        for d in self.dirs:
            if self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] == ' ':
                self.open.append((self.pos[0] + d[0], self.pos[1] + d[1]))

    def RandomSearch(self):
        print("--------You Are Running Random Search--------")
        self.initial()
        count = 1
        while self.open != []:
        #for i in range(10):
            self.pos = random.choice(self.open)
            if count == 1:
                for i in self.open:
                    self.prev[i]= self.start
            self.mazepath[self.pos[1]][self.pos[0]] = '1'
            self.drawPath()
            if self.pos == self.end:
                self.path = self.ReconstructPath()
                for p in self.path:
                    self.drawBox(p[0] * self.boxwidth + self.boxwidth / 2,
                         -p[1] * self.boxwidth + self.boxwidth / 2, "yellow")
                print("steps:", count)
                return
            for d in self.dirs:
                if self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] == ' ':
                    self.open.append((self.pos[0] + d[0], self.pos[1] + d[1]))
                    self.prev[(self.pos[0] + d[0], self.pos[1] + d[1])] = self.pos
                    self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] = '1'
            self.open.remove(self.pos)
            self.closed.append(self.pos)
            count += 1

    def ReconstructPath(self):
        x = self.end
        path = []
        while x != self.start:
            path.append(x)
            x = self.prev[x]
        return path

    def DepthFirstSearch(self):
        print("--------You Are Running Depth First Search Search--------")
        self.initial()
        count = 1
        while self.open != []:
        #for i in range(10):
            if count == 1:
                for i in self.open:
                    self.prev[i] = self.start
            self.mazepath[self.pos[1]][self.pos[0]] = '1'
            self.drawPath()
            self.pos = self.open.pop()
            if self.pos == self.end:
                self.path = self.ReconstructPath()
                for p in self.path:
                    self.drawBox(p[0] * self.boxwidth + self.boxwidth / 2,
                                 -p[1] * self.boxwidth + self.boxwidth / 2, "yellow")
                print("steps:", count)
                return
            for d in self.dirs:
                if self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] == ' ':
                    self.open.append((self.pos[0] + d[0], self.pos[1] + d[1]))
                    self.prev[(self.pos[0] + d[0], self.pos[1] + d[1])] = self.pos
                    self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] = '1'
            self.closed.append(self.pos)
            count += 1

    def WidthFirstSearch (self):
        print("--------You Are Running Width First Search--------")
        self.initial()
        count = 1
        while self.open != []:
            # for i in range(10):
            if count == 1:
                for i in self.open:
                    self.prev[i] = self.start
            self.mazepath[self.pos[1]][self.pos[0]] = '1'
            self.drawPath()
            self.pos = self.open.pop(0)
            if self.pos == self.end:
                self.path = self.ReconstructPath()
                for p in self.path:
                    self.drawBox(p[0] * self.boxwidth + self.boxwidth / 2,
                                 -p[1] * self.boxwidth + self.boxwidth / 2, "yellow")
                print ("steps:",count)
                return
            for d in self.dirs:
                if self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] == ' ':
                    self.open.append((self.pos[0] + d[0], self.pos[1] + d[1]))
                    self.prev[(self.pos[0] + d[0], self.pos[1] + d[1])] = self.pos
                    self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] = '1'
            self.closed.append(self.pos)
            count += 1

    def GreedySearch(self):
        print("--------You Are Running Greedy Search--------")
        self.initial()
        count = 1
        while self.open != []:
            if count == 1:
                for i in self.open:
                    self.prev[i] = self.start
            self.mazepath[self.pos[1]][self.pos[0]] = '1'
            self.drawPath()
            self.pos = self.open.pop(0)
            if self.pos == self.end:
                self.path = self.ReconstructPath()
                for p in self.path:
                    self.drawBox(p[0] * self.boxwidth + self.boxwidth / 2,
                                 -p[1] * self.boxwidth + self.boxwidth / 2, "yellow")
                print("steps:", count)
                return
            random.shuffle(self.dirs)
            for d in self.dirs:
                if self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] == ' ':
                    self.open.insert(0,(self.pos[0] + d[0], self.pos[1] + d[1])) #find the shortest node to itself.
                    # however, since there is not distance for every nodes, just simply chose for the first one of next_directions
                    self.prev[(self.pos[0] + d[0], self.pos[1] + d[1])] = self.pos
                    self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] = '1'
            self.closed.append(self.pos)
            count += 1

    def ASearch(self):
        print("--------You Are Running A*--------")
        self.closed = [self.pos]
        self.mazepath[self.start[1]][self.start[0]] = '1'
        dist = {}
        for d in self.dirs:
            if self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] == ' ':
                self.open.append((self.pos[0] + d[0], self.pos[1] + d[1]))
                dist[(self.pos[0] + d[0], self.pos[1] + d[1])] = 0
                self.prev[(self.pos[0] + d[0], self.pos[1] + d[1])] = self.start
        count = 1

        while self.open != []:
            self.mazepath[self.pos[1]][self.pos[0]] = '1'
            self.drawPath()
            self.pos = self.open.pop(0)
            if self.pos == self.end:
                self.path = self.ReconstructPath()
                for p in self.path:
                    self.drawBox(p[0] * self.boxwidth + self.boxwidth / 2,
                                 -p[1] * self.boxwidth + self.boxwidth / 2, "yellow")
                print("steps:", count)
                return
            for d in self.dirs:
                if self.mazepath[self.pos[1] + d[1]][self.pos[0] + d[0]] == ' ':
                    y = (self.pos[0] + d[0],self.pos[1] + d[1])
                    if y not in self.closed:
                        dis = dist[self.pos] + 1 # distance between every node is 1
                        if y not in dist:
                            dist[y] = 100000
                        if y not in self.open and dist[y] > dis:
                            dist[y] = dis
                            self.prev[y] = self.pos
                            #self.open.insert(0,y)
                            self.open.append(y)
                            self.mazepath[y[1]][y[0]] = '1'
            self.closed.append(self.pos)
            count += 1

    def run(self):
        self.read_maze()
        self.drawMaze()
        if self.alg == 0:
            self.RandomSearch()
        elif self.alg == 1:
            self.DepthFirstSearch()
        elif self.alg == 2:
            self.WidthFirstSearch()
        elif self.alg == 3:
            self.GreedySearch()
        elif self.alg == 4:
            self.ASearch()
        else:
            print("Wrong input")
            return
        print(self.alg)
        self.drawBox(self.start[0]*self.boxwidth+self.boxwidth / 2,-self.start[1]*self.boxwidth+self.boxwidth / 2,"red")
        self.drawBox(self.end[0]*self.boxwidth + self.boxwidth / 2, -self.end[1]*self.boxwidth + self.boxwidth / 2, "blue")

if __name__ == '__main__':
    dataset_path="dataset/"
    dataset=os.listdir(dataset_path)
    for i in range(len(dataset)):
        print(i,":",dataset[i])
    choosing = int(input("Enter a number to choose a maze\n"))
    print("You are choosing: ",dataset[choosing])

    als = ['Random Search','Depth First Search','Width First Search','Greedy Search','A*']
    for i in range(len(als)):
        print(i,":",als[i])
    choosing_alg = int(input("Enter a number to choose an algorithm\n"))
    print("You are choosing: ", als[choosing_alg])

    filepath = dataset_path+dataset[choosing]
    myMaze = Maze(filepath,choosing_alg)
    myMaze.run()
    turtle.mainloop()
# Yiqing Li
# 2023/05/02
# =============================
import copy
import random
import matplotlib.pyplot as plt
import time

N = 30 # number of empty cells

#-----automatically generate a sudoku puzzle-----
def generate_full_sudoku():
    sudoku = [[0 for i in range(9)] for j in range(9)]

    # randomly generate the first row and column in this sudoku
    first_row = [(i+1) for i in range(9)]
    random.shuffle(first_row)
    sudoku[0] = first_row

    # insert numbers row by row using CSP
    solve_CSP(sudoku)
    return sudoku

def generate_solution(sudoku, method):
    if method == 'CSP':
        solve_CSP(sudoku)
    elif method == 'My':
        solve_my(sudoku)
    return sudoku

def create_puzzle(sudoku,n):
    # empty n cells on the filled sudoku to create a puzzle
    numbers = [i for i in range(80)]
    indexs = random.sample(numbers, n)
    for i in indexs:
        row = i // 9
        col = i % 9
        sudoku[row][col] = 0
    return sudoku

def solve_CSP(sudoku):
    # find an empty cell
    row, col = find_empty_cell(sudoku)
    if row == None:
        return True

    #numbers = [i for i in range(1,10)]
    for num in range(1,10):
        if check_constraints(sudoku, row, col, num):
            sudoku[row][col] = num
            if solve_CSP(sudoku): # If all cells are filled, end the loop and return True
                return True
            sudoku[row][col] = 0 # Necessary!! Without this code, there may not be a correct solution

    return False

def solve_my(sudoku):
    # My method tries to find all possible solutions for every cell,
    # and fill the cells from which has the least solutions.
    empty = find_all_empty_cell(sudoku)
    if empty == []:
        return True

    numbers = [i for i in range(1,10)]
    cell_dict = {}
    for cell in empty:
        for num in numbers:
            possible = []
            if check_constraints(sudoku, cell[0], cell[1], num):
                possible.append(num)
            cell_dict[cell[0], cell[1]] = possible
    sorted_keys = sorted(cell_dict, key=lambda k: len(cell_dict[k]), reverse=False)
    #print(sorted_keys)
    for key in sorted_keys:
        solutions = cell_dict[key]
        for num in solutions:
            if check_constraints(sudoku, key[0], key[1], num):
                sudoku[key[0]][key[1]] = num
                if solve_CSP(sudoku):  # If all cells are filled, end the loop and return True
                    return True
                sudoku[key[0]][key[1]] = 0  # Necessary!! Without this code, there may not be a correct solution
    return False

def find_empty_cell(sudoku):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                return row,col
    return None, None

def find_all_empty_cell(sudoku):
    empty = []
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                empty.append([row,col])
    return empty

def check_constraints(sudoku, row, col, num):
    # check the numbers in the same row and column
    for i in range(9):
        if sudoku[row][i] == num:
            return False
        if sudoku[i][col] == num:
            return False

    # check the numbers in the same 3x3 square
    square_row = row//3
    square_col = col//3
    for i in range(square_row*3, square_row*3 + 3):
        for j in range(square_col*3, square_col*3 + 3):
            if sudoku[i][j] == num:
                return False
    return True

def visualize(puzzle,solution1,solution2,time1,time2):
    fig, (ax1, ax2, ax3) = plt.subplots(nrows = 1, ncols = 3, figsize = (15,5))

    fig.suptitle(f"N = {N}")

    ax1.set_xticks([i for i in range(10)])
    ax1.set_yticks([i for i in range(10)])
    ax1.set_title('Puzzle')
    ax1.grid(True, color='black', linewidth=1)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                ax1.text(j+0.5, i+0.5, str(puzzle[i][j]), fontsize=20,
                         horizontalalignment='center', verticalalignment='center', color='black')

    ax2.set_xticks([i for i in range(10)])
    ax2.set_yticks([i for i in range(10)])
    ax2.set_title(f'CSP Solution, time: {time1:.12f}')
    ax2.grid(True, color='black', linewidth=1)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                ax2.text(j + 0.5, i + 0.5, str(solution1[i][j]), fontsize=20,
                         horizontalalignment='center', verticalalignment='center', color='black')
            else:
                ax2.text(j + 0.5, i + 0.5, str(solution1[i][j]), fontsize=20,
                         horizontalalignment='center', verticalalignment='center', color='red')

    ax3.set_xticks([i for i in range(10)])
    ax3.set_yticks([i for i in range(10)])
    ax3.set_title(f'My Solution, time: {time2:.12f}')
    ax3.grid(True, color='black', linewidth=1)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                ax3.text(j + 0.5, i + 0.5, str(solution2[i][j]), fontsize=20,
                         horizontalalignment='center', verticalalignment='center', color='black')
            else:
                ax3.text(j + 0.5, i + 0.5, str(solution2[i][j]), fontsize=20,
                         horizontalalignment='center', verticalalignment='center', color='blue')
    plt.show()

def check_puzzle_valid(sudoku):
    empty_row, empty_col = find_empty_cell(sudoku)
    if empty_row == None:
        return True
    return False

full_sudoku = generate_full_sudoku()
while check_puzzle_valid(full_sudoku)==False:
    full_sudoku = generate_full_sudoku()
puzzle = create_puzzle(full_sudoku,N)

# solve this puzzle
solution1 = copy.deepcopy(puzzle)
solution2 = copy.deepcopy(puzzle)

# track time
start1 = time.time()
solution1 = generate_solution(solution1,'CSP')
end1 = time.time()
using1 = end1 - start1

start2 = time.time()
solution2 = generate_solution(solution2,'My')
end2 = time.time()
using2 = end2 -start2
#print(f"Time when using CSP method: {using1:.12f}.\nTime when using my method: {using2:.12f}")

#print(puzzle)
#print(solution)
visualize(puzzle, solution1,solution2,using1,using2)
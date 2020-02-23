import config
import random

# functions for sudoku


def check_tile(new, y, x, matrix):
    # horizontal and vertical
    for i in range(9):
        if matrix[i][x] == new:
            return False
        elif matrix[y][i] == new:
            return False

    x -= x % 3
    y -= y % 3
    # checking the square
    for i in range(3):
        for j in range(3):
            if matrix[i + y][j + x] == new:
                return False
    return True


def shuffle_array(array):
    length = len(array)
    for i in range(config.SHUFFLE_POWER):
        x1 = random.randrange(length)
        x2 = random.randrange(length)
        if x1 != x2:
            temp = array[x1]
            array[x1] = array[x2]
            array[x2] = temp
    return array


def insert_into_matrix(matrix, array, x, y):
    # writes values from 1d array into 2d matrix
    for i in range(3):
        for j in range(3):
            matrix[x + i][y + j] = array[i * 3 + j]


def create_puzzle():
    # returns an matrix of numbers
    sudoku = []
    matrix = []
    # creating empty sudoku
    for i in range(9):
        temp_array = []
        for j in range(9):
            temp_array.append(0)
        matrix.append(temp_array)

    # creating corner squares
    for i in range(3):
        temp_array = []
        for j in range(1,10):
            temp_array.append(j)
        temp_array = shuffle_array(temp_array)
        insert_into_matrix(matrix, temp_array, 3 * i, 3 * i)

    solution_found = False


    def solve_sudoku(matrix):
        nonlocal solution_found, sudoku
        for i in range(9):
            for j in range(9):
                if matrix[i][j] == 0:
                    for num in range(1,10):
                        if check_tile( num, i, j, matrix):
                            matrix[i][j] = num
                            solve_sudoku(matrix)
                            if solution_found:
                                return
                            matrix[i][j] = 0
                    return
        sudoku = matrix
        solution_found = True

    solve_sudoku(matrix)
    return sudoku


def set_sudoku(sudoku, difficulty):
    for i in range(difficulty):
        rand_row = random.randrange(9)
        rand_num = random.randrange(9)
        sudoku[rand_row][rand_num] = 0
    return sudoku

def click_detect(position):
    # detect if button is pressed then return coordinates of tile in matrix
    x, y = position[0], position[1]
    x -= config.TILE_X_OFFSET
    y -= config.TILE_Y_OFFSET
    x -= ( x // (config.TILE_WIDTH * 3)) * config.INNER_BORDER_LENGTH
    y -= ( y // (config.TILE_HEIGHT * 3)) * config.INNER_BORDER_LENGTH
    y = y // (config.TILE_HEIGHT + 1)
    x = x // (config.TILE_WIDTH + 1)
    if x < 0: x = 0
    if y < 0: y = 0
    return x, y


def set_position(offset, constant, multiplier):
    position = (offset + (constant + 1) * multiplier
        + config.INNER_BORDER_LENGTH * (multiplier // 3))
    return position


def check_win(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0: return False;
    return True


def get_hint(sudoku):
    x0 = random.randrange(9)
    y0 = random.randrange(9)
    while sudoku[y0][x0] != 0:
        x0 = random.randrange(9)
        y0 = random.randrange(9)
    return x0, y0


def get_time_str(sec):
    # gets num of sec and returns time in format "MM : SS"
    # seconds
    sec_str1 = str(sec % 10) # first digit
    sec_str2 = str((sec % 60) // 10) # decimal digit

    # minutes
    min_str1 = sec // 60 % 10 # first digit
    min_str2 = sec // 60 // 10 # decimal digit
    if min_str2 >= 6: return "00 : 00" # after an hour timer is 0

    return "{}{} : {}{}".format(min_str2, min_str1, sec_str2, sec_str1)

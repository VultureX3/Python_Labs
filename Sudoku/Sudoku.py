import random


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) +
                      ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    lines = []
    cur_val = cur_line = 0
    while cur_val < n * n - 1:
        lines.append([])
        for i in range(n):
            lines[cur_line].append(values[cur_val])
            cur_val += 1
        cur_line += 1
    return lines


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return (values[pos[0]])


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for row in values:
        col.append(row[pos[1]])
    return col


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos """
    block = []
    for i in range(9):
        for j in range(9):
            if i // 3 == pos[0] // 3 and j // 3 == pos[1] // 3:
                block.append(values[i][j])
    return block


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'],
    ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'],
    ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'],
    ['.', '8', '9']])
    (2, 0)
    """
    row_num = 0
    for row in grid:
        col_num = 0
        for cell in row:
            if cell == '.':
                return (row_num, col_num)
            col_num += 1
        row_num += 1
    return (-1, -1)


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции """
    options = []
    for i in range(9):
        options.append(True)
    num_row = get_row(grid, pos)
    num_col = get_col(grid, pos)
    num_block = get_block(grid, pos)
    for i in num_row:
        if i != '.':
            options[int(i) - 1] = False
    for i in num_col:
        if i != '.':
            options[int(i) - 1] = False
    for i in num_block:
        if i != '.':
            options[int(i) - 1] = False
    options_num = []
    for i in range(9):
        if options[i] is True:
            options_num.append(str(i + 1))
    return (options_num)


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения,
        которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    """
    pos = find_empty_positions(grid)
    if pos == (-1, -1):
        return (grid)
    options = find_possible_values(grid, pos)
    for i in options:
        grid[pos[0]][pos[1]] = i
        if solve(grid) != 0:
            return solve(grid)
        else:
            grid[pos[0]][pos[1]] = '.'
    return 0


def check_solution(solution):
    """ Если решение solution верно, то вернуть True,
    в противном случае False """
    for i in range(9):
        for j in range(9):
            solution[i][j] = int(solution[i][j])
    for i in range(9):
        for j in range(9):
            num = (get_row(solution, (i, j)) + get_col(solution, (i, j)) +
                   get_block(solution, (i, j)))
            for k in num:
                if num.count(k) != 3:
                    return False
    return True


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt', 'puzzle4.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)

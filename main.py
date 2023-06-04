import random


class SudokuGenerator:
    def __init__(self):
        self.diff = None
        self.grid = [[0 for _ in range(9)] for _ in range(9)]  # Creating an empty grid

    def generate_sudoku(self):
        self.solve_sudoku()  # Using sudoku solving function to generate it

        if self.diff == 2:
            self.remove_cells(50)  # Advanced mode
        elif self.diff == 3:
            self.remove_cells(60)  # Hard mode
        elif self.diff == 4:
            self.remove_cells(70)  # Veteran mode
        else:
            self.remove_cells(40)  # Easy mode

    def solve_sudoku(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell

        for _ in range(1, 10):
            num = random.randrange(1, 10)
            if self.is_valid(row, col, num):
                self.grid[row][col] = num

                if self.solve_sudoku():
                    return True

                self.grid[row][col] = 0

        return False

    def find_empty_cell(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.grid[row][i] == num:
                return False

        for i in range(9):
            if self.grid[i][col] == num:
                return False

        start_row = (row // 3) * 3  # For 0, 1, 2 = 0 / 3, 4, 5 = 3 / 4, 5, 6 = 6
        start_col = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False

        return True

    def remove_cells(self, num_cells):
        cells_removed = 0
        while cells_removed < num_cells:
            row = random.randrange(9)
            col = random.randrange(9)

            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                cells_removed += 1

        return self.grid

    def check_if_solved(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    print("Sudoku niedokończone")
                    return False

                backup = self.grid[i][j]
                self.grid[i][j] = 0

                if not self.is_valid(i, j, backup):
                    print("Sudoku rozwiązane niepoprawnie")
                    self.grid[i][j] = backup
                    return False

                self.grid[i][j] = backup

        print("Sudoku rozwiązane poprawnie!")
        return True

    def print_sudoku(self):
        for row in self.grid:
            print(" ".join(map(str, row)))

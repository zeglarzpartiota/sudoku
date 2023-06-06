import tkinter as tk
import tkinter.messagebox as messagebox
import random


class SudokuGenerator:
    def __init__(self, master):
        self.grid2 = [[0 for _ in range(9)] for _ in range(9)]
        self.number_buttons = []
        self.difficulty = 40
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.master = master
        self.master.title("Sudoku Generator")
        self.master.geometry("540x694")
        self.master.resizable(False, False)
        self.master.configure(bg="white")
        self.canvas = tk.Canvas(self.master, width=540, height=540, bg="#424549")
        self.canvas.pack()
        self.cell_size = 540 // 9

        self.draw_grid()
        self.create_number_buttons()
        self.create_generate_button()
        self.create_check_button()

        # Pasek menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        level_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Poziom trudności", menu=level_menu)

        level_menu.add_command(label="Easy", command=self.set_difficulty_easy)
        level_menu.add_command(label="Advanced", command=self.set_difficulty_advanced)
        level_menu.add_command(label="Hard", command=self.set_difficulty_hard)
        level_menu.add_command(label="Veteran", command=self.set_difficulty_veteran)

        self.selected_row = None
        self.selected_col = None

    def draw_grid(self):
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, 540, width=line_width, fill="white")
            self.canvas.create_line(0, i * self.cell_size, 540, i * self.cell_size, width=line_width, fill="white")

        self.canvas.bind("<Button-1>", self.select_cell)

    def create_number_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        for i in range(1, 10):
            button = tk.Button(button_frame, text=str(i), width=5, height=2, fg="white", bg="#36393e",
                               activebackground="#61656b", font=("Arial", 10, "bold"))
            button.grid(row=0, column=i - 1, padx=5, pady=5)
            button.bind("<Button-1>",
                        lambda event, num=i: self.place_number(num))
            self.number_buttons.append(button)

    def create_generate_button(self):
        generate_button = tk.Button(self.master, text="Generuj nowe sudoku", width=51, command=self.generate_sudoku,
                                    fg="white", bg="#36393e", activebackground="#61656b", font=("Arial", 12, "bold"))
        generate_button.pack(pady=10)

    def create_check_button(self):
        check_button = tk.Button(self.master, text="Sprawdź sudoku", width=485, command=self.check_if_solved,
                                 bg="#36393e", fg="white", activebackground="#61656b", font=("Arial", 12, "bold"))
        check_button.pack(padx=10)

    def generate_sudoku(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.canvas.delete("all")
        self.solve_sudoku()
        self.remove_cells()
        self.draw_grid()

        for row in range(9):
            for col in range(9):
                cell_value = self.grid[row][col]
                if cell_value != 0:
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 18, "bold"), fill="white")

        self.grid2 = self.grid

    def solve_sudoku(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell
        nums = random.sample(range(1, 10), 9)

        for num in nums:
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
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False

        return True

    def remove_cells(self):
        cells_removed = 0
        while cells_removed < self.difficulty:
            row = random.randrange(9)
            col = random.randrange(9)

            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                cells_removed += 1

    def check_if_solved(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    messagebox.showinfo("Sudoku niedokończone", "Sudoku jest niedokończone!")
                    return False

                backup = self.grid[i][j]
                self.grid[i][j] = 0

                if not self.is_valid(i, j, backup):
                    self.grid[i][j] = backup
                    messagebox.showinfo("Sudoku rozwiązane niepoprawnie", "Sudoku zostało rozwiązane niepoprawnie!")
                    return False

                self.grid[i][j] = backup

        messagebox.showinfo("Gratulacje!", "Sudoku zostało rozwiązane poprawnie!")
        return True

    def set_difficulty_easy(self):
        self.difficulty = 40
        return self.difficulty

    def set_difficulty_advanced(self):
        self.difficulty = 50
        return self.difficulty

    def set_difficulty_hard(self):
        self.difficulty = 60
        return self.difficulty

    def set_difficulty_veteran(self):
        self.difficulty = 70
        return self.difficulty

    def select_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        self.canvas.delete("highlight")
        self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size,
                                     (col + 1) * self.cell_size, (row + 1) * self.cell_size,
                                     outline="yellow", width=2, tags="highlight")

        self.selected_row = row
        self.selected_col = col

    def place_number(self, num):
        if self.selected_row is not None and self.selected_col is not None:
            if self.grid2[self.selected_row][self.selected_col] == 0:
                self.grid[self.selected_row][self.selected_col] = num
                self.canvas.delete("all")
                self.draw_grid()

                for row in range(9):
                    for col in range(9):
                        cell_value = self.grid[row][col]
                        if cell_value != 0:
                            x = col * self.cell_size + self.cell_size // 2
                            y = row * self.cell_size + self.cell_size // 2
                            self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 18, "bold"),
                                                    fill="white")


root = tk.Tk()
sudoku_gui = SudokuGenerator(root)
root.mainloop()

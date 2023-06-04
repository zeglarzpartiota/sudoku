import tkinter as tk
from main import *


class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.diff = None
        self.master.title("Sudoku Generator")
        self.master.geometry("540x694")  # Zmiana rozmiaru okna na 540x680
        self.master.resizable(False, False)  # Blokowanie zmiany rozmiaru okna
        self.master.configure(bg="white")

        self.sudoku_generator = SudokuGenerator()

        # Pasek menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # Zakładka "Poziom trudności"
        level_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Poziom trudności", menu=level_menu)

        # Elementy wewnątrz zakładki "Poziom trudności"
        level_menu.add_command(label="Easy", command=self.set_difficulty_easy)
        level_menu.add_command(label="Advanced", command=self.set_difficulty_advanced)
        level_menu.add_command(label="Hard", command=self.set_difficulty_hard)
        level_menu.add_command(label="Veteran", command=self.set_difficulty_veteran)

        self.canvas = tk.Canvas(self.master, width=540, height=540, bg="#424549")
        self.canvas.pack()

        self.cell_size = 540 // 9
        self.grid = [[0 for _ in range(9)] for _ in range(9)]  # Pusta plansza Sudoku

        self.draw_grid()
        self.create_number_buttons()
        self.create_generate_button()  # Dodanie przycisku generowania nowego Sudoku
        self.create_check_button()  # Dodanie przycisku sprawdzania Sudoku

    def draw_grid(self):
        for i in range(10):
            if i % 3 == 0:
                line_width = 4
            else:
                line_width = 1

            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, 540, width=line_width, fill="white")
            self.canvas.create_line(0, i * self.cell_size, 540, i * self.cell_size, width=line_width, fill="white")

    def create_number_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        for i in range(1, 10):
            button = tk.Button(button_frame, text=str(i), width=5, height=2, fg="white", bg="#36393e",
                               activebackground="#61656b", font=("Arial", 10, "bold"))
            button.grid(row=0, column=i - 1, padx=5, pady=5)

    def create_generate_button(self):
        generate_button = tk.Button(self.master, text="Generuj nowe sudoku", width=51, command=self.generate_sudoku,
                                    fg="white", bg="#36393e", activebackground="#61656b", font=("Arial", 12, "bold"))
        generate_button.pack(pady=10)

    def create_check_button(self):
        check_button = tk.Button(self.master, text="Sprawdź sudoku", width=485, command=self.check_sudoku, bg="#36393e",
                                 fg="white", activebackground="#61656b", font=("Arial", 12, "bold"))
        check_button.pack(padx=10)

    def generate_sudoku(self):
        self.canvas.delete("all")  # Usunięcie wszystkich elementów z canvasa
        self.sudoku_generator.generate_sudoku()
        self.grid = self.sudoku_generator.grid
        self.draw_grid()

        for row in range(9):
            for col in range(9):
                cell_value = self.grid[row][col]
                if cell_value != 0:
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 18, "bold"), fill="white")

    def check_sudoku(self):
        pass

    def set_difficulty_easy(self):
        self.sudoku_generator.diff = 1
        return self.sudoku_generator.diff

    def set_difficulty_advanced(self):
        self.sudoku_generator.diff = 2
        return self.sudoku_generator.diff

    def set_difficulty_hard(self):
        self.sudoku_generator.diff = 3
        return self.sudoku_generator.diff

    def set_difficulty_veteran(self):
        self.sudoku_generator.diff = 4
        return self.sudoku_generator.diff


if __name__ == "__main__":
    root = tk.Tk()
    sudoku_gui = SudokuGUI(root)
    root.mainloop()

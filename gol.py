import tkinter as tk
from tkinter import Label, Button, Canvas, Frame, Scale

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.cell_size = 20
        self.is_running = False
        self.speed = 1

        # frame on top of grid Canvas to contain the controls
        self.frame = Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill="both", expand=True)

        self.grid = []
        self.width = 0
        self.height = 0

        self.create_control_panel()
        
        self.master.bind("<Configure>", self.on_resize) # on window resize
        self.canvas.bind("<Button-1>", self.toggle_cell) # on grid click

        # Initial draw with 100ms delay PYTHON UI ISSUES
        self.master.after(100, self.initialize_grid)

    def initialize_grid(self):
        self.on_resize(None)
        self.draw_grid()


    def on_resize(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            self.width = canvas_width // self.cell_size
            self.height = canvas_height // self.cell_size

            # TODO Preserve old entries somehow
            # Only reinitialize the grid if the size has changed
            if len(self.grid) != self.height or (self.grid and len(self.grid[0]) != self.width):
                self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
            
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.height):
            for j in range(self.width):
                # Calc Box cordinates 
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # IS box clicked????? => black
                fill = "white" if self.grid[i][j] == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

    def toggle_cell(self, event):
        # find location
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        # redraw grid
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 1 - self.grid[row][col]
            self.draw_grid()

    def create_control_panel(self):
        self.control_panel = Frame(self.frame, bg=None)
        self.control_panel.pack(side='bottom', fill='x')

        self.play_pause_button = Button(self.control_panel, text="Play", command=self.toggle_play_pause)
        self.play_pause_button.pack(side='left', padx=5, pady=5)

        self.next_frame_button = Button(self.control_panel, text="Next Frame", command=self.next_frame)
        self.next_frame_button.pack(side='left', padx=5, pady=5)

        self.clear_button = Button(self.control_panel, text="Clear", command=self.clear_grid)
        self.clear_button.pack(side='left', padx=5, pady=5)

        self.speed_scale = Scale(self.control_panel, from_=1, to=10, orient='horizontal', label='Speed',
                                 command=self.update_speed)
        self.speed_scale.set(5)  # Set default speed to middle value
        self.speed_scale.pack(side='right', padx=5, pady=5)

    def toggle_play_pause(self):
        self.is_running = not self.is_running
        self.play_pause_button.config(text="Pause" if self.is_running else "Play")
        self.master.after(10, self.draw_grid)
        # TODO auto run next frame
        if self.is_running:
            self.run_game()

    def run_game(self):
        if self.is_running:
            self.next_frame()
            self.master.after(int(1000 / self.speed), self.run_game)

    def next_frame(self):
        # fork and redraw
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    if neighbors in [2, 3]:
                        new_grid[i][j] = 1
                else:
                    if neighbors == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid
        self.draw_grid()

    def count_neighbors(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = (row + i) % self.height
                c = (col + j) % self.width
                count += self.grid[r][c]
        return count

    def clear_grid(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.draw_grid()

    def update_speed(self, val):
        self.speed = float(val)

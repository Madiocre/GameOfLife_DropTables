import customtkinter as ctk
import pygame
from pygame import mixer
from utils import resource_path
class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.cell_size = 20
        self.is_running = False
        self.speed = 1
        self.is_selecting = False
        self.last_cell = None

        # pygame for audio :D
        pygame.mixer.init()
        self.background_music = mixer.Sound(resource_path("assets/music/s3.wav"))
        self.click_sound = mixer.Sound(resource_path("assets/music/s2.wav"))
        self.remove_sound = mixer.Sound(resource_path("assets/music/s1.wav"))

        # self.background_music.play(-1)  # loop

        # frame on top of grid Canvas to contain the controls
        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(self.frame, bg="gray10", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        self.grid = []
        self.width = 0
        self.height = 0

        self.create_control_panel()
        
        self.master.bind("<Configure>", self.on_resize) # on window resize
        # hover listeners
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

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
                # Calc Box coordinates 
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # IS box clicked????? => black
                fill = "gray10" if self.grid[i][j] == 0 else "cyan"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray30")

    def create_control_panel(self):
        self.control_panel = ctk.CTkFrame(self.frame)
        self.control_panel.pack(fill="x", padx=20, pady=10)

        self.play_pause_button = ctk.CTkButton(
            self.control_panel,
            text="Play",
            command=self.toggle_play_pause,
            width=100
        )
        self.play_pause_button.pack(side="left", padx=(0, 10))

        self.next_frame_button = ctk.CTkButton(
            self.control_panel,
            text="Next Frame",
            command=self.next_frame,
            width=100
        )
        self.next_frame_button.pack(side="left", padx=10)

        self.clear_button = ctk.CTkButton(
            self.control_panel,
            text="Clear",
            command=self.clear_grid,
            width=100
        )
        self.clear_button.pack(side="left", padx=10)

        self.speed_label = ctk.CTkLabel(self.control_panel, text="Speed:")
        self.speed_label.pack(side="left", padx=(20, 5))

        self.speed_slider = ctk.CTkSlider(
            self.control_panel,
            from_=1,
            to=10,
            number_of_steps=9,
            command=self.update_speed
        )
        self.speed_slider.pack(side="left", padx=(0, 20), expand=True, fill="x")
        self.speed_slider.set(5)

    def toggle_play_pause(self):
        self.is_running = not self.is_running
        self.play_pause_button.configure(text="Pause" if self.is_running else "Play")
        self.master.after(10, self.draw_grid)
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
        self.remove_sound.play()

    def update_speed(self, val):
        self.speed = float(val)

    def start_selection(self, event):
        self.is_selecting = True
        self.last_cell = (event.y // self.cell_size, event.x // self.cell_size)
        self.toggle_cell(event)

    def update_selection(self, event):
        if self.is_selecting:
            current_cell = (event.y // self.cell_size, event.x // self.cell_size)
            self.fill_cells_between(self.last_cell, current_cell)
            self.last_cell = current_cell
            self.draw_grid()

    def fill_cells_between(self, start, end):
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if 0 <= x0 < self.height and 0 <= y0 < self.width:
                self.grid[x0][y0] = 1
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def end_selection(self, event):
        self.is_selecting = False
        self.click_sound.play()

    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 1 - self.grid[row][col]
            self.draw_grid()
            if self.grid[row][col] == 1:
                self.click_sound.play()
            else:
                self.remove_sound.play()

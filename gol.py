import tkinter as tk
from tkinter import Label, Button, Canvas, Frame, Scale
import pygame
from pygame import mixer

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
        self.background_music = mixer.Sound("assets/music/s3.wav")
        self.click_sound = mixer.Sound("assets/music/s2.wav")
        self.remove_sound = mixer.Sound("assets/music/s1.wav")

        # self.background_music.play(-1)  # loop

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
        # hover listners
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        # Initial draw with 100ms delay PYTHON UI ISSUES
        self.master.after(100, self.initialize_grid)

    def initialize_grid(self):
        self.on_resize(None)
        self.draw_grid()


    # Modified to preserve grid state when resizing
    def on_resize(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            new_width = canvas_width // self.cell_size
            new_height = canvas_height // self.cell_size

            # Only update the grid if the size has changed
            if new_width != self.width or new_height != self.height:
                new_grid = [[0 for _ in range(new_width)] for _ in range(new_height)]
                
                # Copy existing grid data to new grid
                for i in range(min(self.height, new_height)):
                    for j in range(min(self.width, new_width)):
                        new_grid[i][j] = self.grid[i][j]
                
                self.grid = new_grid
                self.width = new_width
                self.height = new_height
            
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.height):
            for j in range(self.width):
                self.draw_cell(i, j)
    
    # New method to draw individual cells
    def draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        fill = "black" if self.grid[row][col] == 1 else "white"
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="gray")

    def start_selection(self, event):
        # on box drag + hover
        self.is_selecting = True
        self.last_cell = (event.y // self.cell_size, event.x // self.cell_size)
        self.toggle_cell(event)

    def update_selection(self, event):
        # while hovering
        if self.is_selecting:
            current_cell = (event.y // self.cell_size, event.x // self.cell_size)
            self.fill_cells_between(self.last_cell, current_cell)
            self.last_cell = current_cell
            self.draw_grid()
            self.click_sound.play()

    def fill_cells_between(self, start, end):
        # calc new boxes enabled
        # use parent box as start point
        # calc coords distance
        # highlight new selected if it's at that location
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
                self.draw_cell(x0, y0)
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
        # click relase
        self.is_selecting = False
        # self.click_sound.play()

    def toggle_cell(self, event):
        # find location
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 1 - self.grid[row][col]
            self.draw_cell(row, col)
            if self.grid[row][col] == 0:
                self.remove_sound.play()
            else:
                self.click_sound.play()


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
        
        # New: Add grid size control
        self.grid_size_scale = Scale(self.control_panel, from_=10, to=50, orient='horizontal', label='Grid Size',
                                     command=self.update_grid_size)
        self.grid_size_scale.set(self.cell_size)
        self.grid_size_scale.pack(side='right', padx=5, pady=5)
    
    # New method to handle grid size changes
    def update_grid_size(self, val):
        new_cell_size = int(val)
        if new_cell_size != self.cell_size:
            self.cell_size = new_cell_size
            self.on_resize(None)  # Trigger a resize event to redraw the grid

    def toggle_play_pause(self):
        self.is_running = not self.is_running
        self.play_pause_button.config(text="Pause" if self.is_running else "Play")
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

    def update_speed(self, val):
        self.speed = float(val)

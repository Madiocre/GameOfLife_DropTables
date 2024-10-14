import tkinter as tk
# from tkinter import Label, Button, Canvas, Frame, Scale
from tkinter import Button, Frame, Scale
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

        # Initialize pygame mixer
        pygame.mixer.init()
        self.background_music = mixer.Sound(
            resource_path("assets/music/s3.wav")
            )
        self.click_sound = mixer.Sound(resource_path("assets/music/s2.wav"))
        self.remove_sound = mixer.Sound(resource_path("assets/music/s1.wav"))

        # self.background_music.play(-1)  # loop

        # frame on top of grid Canvas to contain the controls
        self.frame = Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill="both", expand=True)

        # Store active cells in a set
        self.active_cells = set()

        self.create_control_panel()

        self.master.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        self.master.after(100, self.initialize_grid)

    def initialize_grid(self):
        self.on_resize(None)
        self.draw_grid()

    def on_resize(self, event):
        self.width = self.canvas.winfo_width() // self.cell_size
        self.height = self.canvas.winfo_height() // self.cell_size
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.height):
            for j in range(self.width):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill = "black" if (i, j) in self.active_cells else "white"
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="gray"
                    )

    def start_selection(self, event):
        # on box drag + hover
        self.is_selecting = True
        self.last_cell = (event.y // self.cell_size, event.x // self.cell_size)
        self.toggle_cell(event)

    def update_selection(self, event):
        # while hovering
        if self.is_selecting:
            current_cell = (
                event.y //
                self.cell_size, event.x //
                self.cell_size
                )
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
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            if (row, col) in self.active_cells:
                self.active_cells.remove((row, col))
                self.remove_sound.play()
            else:
                self.active_cells.add((row, col))
                self.click_sound.play()
            self.draw_grid()

    def create_control_panel(self):
        self.control_panel = Frame(self.frame, bg=None)
        self.control_panel.pack(side='bottom', fill='x')

        self.play_pause_button = Button(
            self.control_panel, text="Play",
            command=self.toggle_play_pause
            )
        self.play_pause_button.pack(side='left', padx=5, pady=5)

        self.next_frame_button = Button(
            self.control_panel,
            text="Next Frame",
            command=self.next_frame
            )
        self.next_frame_button.pack(side='left', padx=5, pady=5)

        self.clear_button = Button(
            self.control_panel,
            text="Clear",
            command=self.clear_grid
            )
        self.clear_button.pack(side='left', padx=5, pady=5)

        self.speed_scale = Scale(
            self.control_panel,
            from_=1,
            to=10,
            orient='horizontal',
            label='Speed',
            command=self.update_speed
            )
        self.speed_scale.set(5)  # Set default speed to middle value
        self.speed_scale.pack(side='right', padx=5, pady=5)

    def toggle_play_pause(self):
        self.is_running = not self.is_running
        self.play_pause_button.config(
            text="Pause" if self.is_running else "Play"
            )
        self.master.after(10, self.draw_grid)
        if self.is_running:
            self.run_game()

    def run_game(self):
        if self.is_running:
            self.next_frame()
            self.master.after(int(1000 / self.speed), self.run_game)

    def next_frame(self):
        new_active_cells = set()
        cells_to_check = set(self.active_cells)

        # Add all neighbors of active cells to the cells to check
        for cell in self.active_cells:
            cells_to_check.update(self.get_neighbors(*cell))

        for cell in cells_to_check:
            neighbors = self.count_neighbors(*cell)
            if cell in self.active_cells:
                if neighbors in [2, 3]:
                    new_active_cells.add(cell)
            else:
                if neighbors == 3:
                    new_active_cells.add(cell)

        self.active_cells = new_active_cells
        self.draw_grid()

    def count_neighbors(self, row, col):
        count = 0
        for neighbor in self.get_neighbors(row, col):
            if neighbor in self.active_cells:
                count += 1
        return count

    def get_neighbors(self, row, col):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbors.append(((row + i), (col + j)))
        return neighbors

    def clear_grid(self):
        self.active_cells.clear()
        self.draw_grid()

    def update_speed(self, val):
        self.speed = float(val)

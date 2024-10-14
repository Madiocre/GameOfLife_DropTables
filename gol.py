import json
import tkinter as tk
from tkinter import Label, Button, Canvas, Frame, Scale, filedialog
import pygame
from pygame import mixer
from utils import resource_path

class GameOfLife:
    def __init__(self, master, color_palette, muted):
        self.master = master
        self.color_palette = color_palette
        self.cell_size = 20
        self.cell_padding = 1
        self.is_running = False
        self.speed = 1
        self.is_selecting = False
        self.last_cell = None

        self.save_button = None
        self.load_button = None

        # pygame for audio :D
        pygame.mixer.init()
        self.click_sound = mixer.Sound(resource_path("assets/music/s2.wav"))
        self.remove_sound = mixer.Sound(resource_path("assets/music/s1.wav"))
        self.is_muted = muted.get()
        self.update_sound_volume()

        self.frame = Frame(self.master, bg=self.color_palette["primary"])
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, highlightthickness=0, bg=self.color_palette["primary"])
        self.canvas.pack(fill="both", expand=True)

        self.grid = {}
        self.width = 0
        self.height = 0

        self.create_control_panel()
        
        self.master.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        self.master.after(100, self.initialize_grid)

    def update_sound_volume(self):
        volume = 0 if self.is_muted else 1
        self.click_sound.set_volume(volume)
        self.remove_sound.set_volume(volume)

    def initialize_grid(self):
        self.on_resize(None)
        self.draw_grid()

    def on_resize(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            self.width = canvas_width // self.cell_size
            self.height = canvas_height // self.cell_size
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width * self.cell_size, self.height * self.cell_size, 
                                     fill=self.color_palette["primary"], width=0)
        
        # Draw all cells first
        for (row, col) in self.grid:
            self.draw_cell(row, col)
        
        # Draw grid lines on top
        for i in range(0, self.width * self.cell_size + 1, self.cell_size):
            self.canvas.create_line(i, 0, i, self.height * self.cell_size, fill=self.color_palette["accent"])
        for i in range(0, self.height * self.cell_size + 1, self.cell_size):
            self.canvas.create_line(0, i, self.width * self.cell_size, i, fill=self.color_palette["accent"])

    def draw_cell(self, row, col):
        x1 = col * self.cell_size + self.cell_padding
        y1 = row * self.cell_size + self.cell_padding
        x2 = (col + 1) * self.cell_size - self.cell_padding
        y2 = (row + 1) * self.cell_size - self.cell_padding
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.color_palette["secondary"], width=0)

    def start_selection(self, event):
        self.is_selecting = True
        self.last_cell = (event.y // self.cell_size, event.x // self.cell_size)
        self.toggle_cell(event)

    def update_selection(self, event):
        if self.is_selecting:
            current_cell = (event.y // self.cell_size, event.x // self.cell_size)
            if current_cell != self.last_cell:
                self.fill_cells_between(self.last_cell, current_cell)
                self.last_cell = current_cell
                self.click_sound.play()

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
                self.grid[(x0, y0)] = 1
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
        self.draw_grid()  # Redraw the entire grid to ensure grid lines are on top

    def end_selection(self, event):
        self.is_selecting = False

    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            if (row, col) in self.grid:
                del self.grid[(row, col)]
                self.remove_sound.play()
            else:
                self.grid[(row, col)] = 1
                self.draw_cell(row, col)
                self.click_sound.play()
            self.draw_grid()  # Redraw the entire grid to ensure grid lines are on top

    def create_control_panel(self):
        self.control_panel = Frame(self.frame, bg=self.color_palette["primary"])
        self.control_panel.pack(side='bottom', fill='x')

        button_style = {'bg': self.color_palette["secondary"], 'fg': self.color_palette["primary"], 
                        'activebackground': self.color_palette["accent"], 'activeforeground': self.color_palette["primary"]}
        scale_style = {'bg': self.color_palette["primary"], 'fg': self.color_palette["accent"], 
                       'troughcolor': self.color_palette["secondary"], 'activebackground': self.color_palette["secondary"]}

        self.play_pause_button = Button(self.control_panel, text="Play", command=self.toggle_play_pause, **button_style)
        self.play_pause_button.pack(side='left', padx=5, pady=5)

        self.next_frame_button = Button(self.control_panel, text="Next Frame", command=self.next_frame, **button_style)
        self.next_frame_button.pack(side='left', padx=5, pady=5)

        self.clear_button = Button(self.control_panel, text="Clear", command=self.clear_grid, **button_style)
        self.clear_button.pack(side='left', padx=5, pady=5)

        # Add Save and Load buttons
        self.save_button = Button(self.control_panel, text="Save", command=self.save_state, **button_style)
        self.save_button.pack(side='left', padx=5, pady=5)
        self.load_button = Button(self.control_panel, text="Load", command=self.load_state, **button_style)
        self.load_button.pack(side='left', padx=5, pady=5)

        self.speed_scale = Scale(self.control_panel, from_=1, to=10, orient='horizontal', label='Speed',
                                 command=self.update_speed, **scale_style)
        self.speed_scale.set(5)
        self.speed_scale.pack(side='right', padx=5, pady=5)

        self.grid_size_scale = Scale(self.control_panel, from_=5, to=50, orient='horizontal', label='Grid Size',
                                     command=self.update_grid_size, **scale_style)
        self.grid_size_scale.set(self.cell_size)
        self.grid_size_scale.pack(side='right', padx=5, pady=5)

     
    def save_state(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            state = {
                "cell_size": self.cell_size,
                "grid": list(self.grid.keys()),
                "width": self.width,
                "height": self.height
            }
            with open(file_path, "w") as f:
                json.dump(state, f)

    def load_state(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as f:
                state = json.load(f)
            
            self.cell_size = state["cell_size"]
            self.grid = {tuple(cell): 1 for cell in state["grid"]}
            self.width = state["width"]
            self.height = state["height"]
            # Update the grid size scale
            self.grid_size_scale.set(self.cell_size)
            # Redraw the grid
            self.draw_grid()


    def update_grid_size(self, val):
        new_cell_size = int(val)
        if new_cell_size != self.cell_size:
            self.cell_size = new_cell_size
            self.cell_padding = max(1, self.cell_size // 10)
            self.on_resize(None)

    def toggle_play_pause(self):
        self.is_running = not self.is_running
        self.play_pause_button.config(text="Pause" if self.is_running else "Play")
        if self.is_running:
            self.run_game()

    def run_game(self):
        if self.is_running:
            self.next_frame()
            self.master.after(int(1000 / self.speed), self.run_game)

    def next_frame(self):
        new_grid = {}
        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                if (i, j) in self.grid:
                    if neighbors in [2, 3]:
                        new_grid[(i, j)] = 1
                elif neighbors == 3:
                    new_grid[(i, j)] = 1
        
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
                count += (r, c) in self.grid
        return count

    def clear_grid(self):
        self.grid.clear()
        self.draw_grid()

    def update_speed(self, val):
        self.speed = float(val)

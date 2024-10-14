import tkinter as tk
from tkinter import Button, Frame, Scale
import pygame
from pygame import mixer
from utils import resource_path


class GameOfLife:
    """
    A class to represent the Game of Life application.
    """

    def __init__(self, master):
        """
        Initialize the Game of Life application.

        Args:
            master (tk.Tk): The root window of the application.
        """
        self.master = master
        self.cell_size = 20
        self.is_running = False
        self.speed = 5
        self.is_selecting = False
        self.last_cell = None
        self.active_cells = set()

        self.initialize_audio()
        self.setup_ui()
        self.bind_events()

        self.master.after(100, self.initialize_grid)

    def initialize_audio(self):
        """
        Initialize the audio components for the application.
        """
        pygame.mixer.init()
        self.background_music = mixer.Sound(
            resource_path("assets/music/s3.wav")
            )
        self.click_sound = mixer.Sound(resource_path("assets/music/s2.wav"))
        self.remove_sound = mixer.Sound(resource_path("assets/music/s1.wav"))

    def setup_ui(self):
        """
        Set up the user interface components for the application.
        """
        self.frame = Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill="both", expand=True)

        self.create_control_panel()

    def bind_events(self):
        """
        Bind the necessary events for the application.
        """
        self.master.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

    def initialize_grid(self):
        """
        Initialize the grid for the Game of Life.
        """
        self.on_resize(None)
        self.draw_grid()

    def on_resize(self, event):
        """
        Handle the window resize event.

        Args:
            event (tk.Event): The resize event.
        """
        self.width = self.canvas.winfo_width() // self.cell_size
        self.height = self.canvas.winfo_height() // self.cell_size
        self.draw_grid()

    def draw_grid(self):
        """
        Draw the grid for the Game of Life.
        """
        self.canvas.delete("all")
        for i in range(self.height):
            for j in range(self.width):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
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
        """
        Start the cell selection process.

        Args:
            event (tk.Event): The mouse click event.
        """
        self.is_selecting = True
        self.last_cell = (event.y // self.cell_size, event.x // self.cell_size)
        self.toggle_cell(event)

    def update_selection(self, event):
        """
        Update the cell selection process.

        Args:
            event (tk.Event): The mouse drag event.
        """
        if self.is_selecting:
            current_cell = (
                event.y // self.cell_size, event.x // self.cell_size
                )
            self.fill_cells_between(self.last_cell, current_cell)
            self.last_cell = current_cell
            self.draw_grid()
            self.click_sound.play()

    def fill_cells_between(self, start, end):
        """
        Fill the cells between the start and end points.

        Args:
            start (tuple): The starting cell coordinates.
            end (tuple): The ending cell coordinates.
        """
        x0, y0 = start
        x1, y1 = end
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx, sy = 1 if x0 < x1 else -1, 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if 0 <= x0 < self.height and 0 <= y0 < self.width:
                self.active_cells.add((x0, y0))
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
        """
        End the cell selection process.

        Args:
            event (tk.Event): The mouse release event.
        """
        self.is_selecting = False

    def toggle_cell(self, event):
        """
        Toggle the state of a cell.

        Args:
            event (tk.Event): The mouse click event.
        """
        col, row = event.x // self.cell_size, event.y // self.cell_size
        if 0 <= row < self.height and 0 <= col < self.width:
            cell = (row, col)
            if cell in self.active_cells:
                self.active_cells.remove(cell)
                self.remove_sound.play()
            else:
                self.active_cells.add(cell)
                self.click_sound.play()
            self.draw_grid()

    def create_control_panel(self):
        """
        Create the control panel for the application.
        """
        self.control_panel = Frame(self.frame)
        self.control_panel.pack(side='bottom', fill='x')

        buttons = [
            ("Play", self.toggle_play_pause),
            ("Next Frame", self.next_frame),
            ("Clear", self.clear_grid)
        ]

        for text, command in buttons:
            Button(self.control_panel, text=text, command=command).pack(
                side='left',
                padx=5,
                pady=5
                )

        self.speed_scale = Scale(
            self.control_panel,
            from_=1, to=10, orient='horizontal', label='Speed',
            command=self.update_speed
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side='right', padx=5, pady=5)

    def toggle_play_pause(self):
        """
        Toggle the play/pause state of the game.
        """
        self.is_running = not self.is_running
        self.control_panel.children['!button'].config(
            text="Pause" if self.is_running else "Play"
            )
        if self.is_running:
            self.run_game()

    def run_game(self):
        """
        Run the game loop.
        """
        if self.is_running:
            self.next_frame()
            self.master.after(int(1000 / self.speed), self.run_game)

    def next_frame(self):
        """
        Calculate the next frame of the game.
        """
        new_active_cells = set()
        cells_to_check = self.active_cells.union(
            *map(self.get_neighbors, self.active_cells)
            )

        for cell in cells_to_check:
            neighbors = sum(
                neighbor in self.active_cells
                for neighbor in self.get_neighbors(cell)
                )
            if neighbors == 3 or (
                cell in self.active_cells and neighbors == 2
                    ):
                new_active_cells.add(cell)

        self.active_cells = new_active_cells
        self.draw_grid()

    def get_neighbors(self, cell):
        """
        Get the neighbors of a cell.

        Args:
            cell (tuple): The cell coordinates.

        Returns:
            set: A set of neighboring cell coordinates.
        """
        row, col = cell
        return {((row + i) % self.height, (col + j) % self.width)
                for i in (-1, 0, 1) for j in (-1, 0, 1)
                if (i, j) != (0, 0)}

    def clear_grid(self):
        """
        Clear the grid.
        """
        self.active_cells.clear()
        self.draw_grid()

    def update_speed(self, val):
        """
        Update the speed of the game.

        Args:
            val (str): The new speed value.
        """
        self.speed = float(val)

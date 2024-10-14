import tkinter as tk
from tkinter import Label, Canvas, OptionMenu, StringVar, ttk
from PIL import Image, ImageTk
from gol import GameOfLife
from utils import resource_path
import pygame
from pygame import mixer
import random


class MainApplication:
    """
    Main application class for the Game of Life DropTables application.
    Initializes the main window and sets up the UI.
    """
    def __init__(self, root):
        """
        Initializes the MainApplication with the given root window.

        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("Game Of Life DropTables;")
        self.root.geometry("700x500")

        # Set minimum width to 400 and height to 300
        self.root.minsize(400, 300)
        self.color_palettes = {
            "Blue": {"primary": "#1e1e2e", "secondary": "#89b4fa", "accent": "#cdd6f4"},
            "Red": {"primary": "#2e1e1e", "secondary": "#fa8989", "accent": "#f4cdcd"},
            "Yellow": {"primary": "#2e2e1e", "secondary": "#fafa89", "accent": "#f4f4cd"},
            "Green": {"primary": "#1e2e1e", "secondary": "#89fa89", "accent": "#cdf4cd"},
            "Purple": {"primary": "#2e1e2e", "secondary": "#b489fa", "accent": "#e0cdf4"}
        }
        self.selected_palette = StringVar(value=random.choice(list(self.color_palettes.keys())))
        self.audio_file = resource_path("assets/music/lofi_8bit.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play(-1) 
        self.is_muted = tk.BooleanVar(value=False)
        
        self.setup_intro()


    def setup_intro(self):
        self.intro_canvas = tk.Canvas(self.root, bg="black")
        self.intro_canvas.pack(fill="both", expand=True)

        self.logo_image = Image.open(resource_path("assets/img/logo.png"))
        self.logo_image = self.logo_image.resize((200, 200), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_item = self.intro_canvas.create_image(350, 200, image=self.logo_photo, state='hidden')
        self.team_text = self.intro_canvas.create_text(350, 400, text="DropTables Team;\n        Presents", fill="white", font=("Helvetica", 22), state='hidden')

        self.root.after(500, self.fade_in_logo)

    def fade_in_logo(self, alpha=0):
        if alpha < 255:
            alpha += 5
            logo_image = self.logo_image.copy()
            logo_image.putalpha(alpha)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            self.intro_canvas.itemconfig(self.logo_item, image=self.logo_photo, state='normal')
            self.root.after(50, self.fade_in_logo, alpha)
        else:
            self.root.after(500, self.fade_in_team_text)

    def fade_in_team_text(self, alpha=0):
        if alpha < 255:
            alpha += 5
            self.intro_canvas.itemconfig(self.team_text, state='normal', fill=f'#{alpha:02x}{alpha:02x}{alpha:02x}')
            self.root.after(50, self.fade_in_team_text, alpha)
        else:
            self.root.after(1000, self.fade_out_intro)

    def fade_out_intro(self, alpha=255):
        if alpha > 0:
            alpha -= 5
            logo_image = self.logo_image.copy()
            logo_image.putalpha(alpha)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            self.intro_canvas.itemconfig(self.logo_item, image=self.logo_photo)
            self.intro_canvas.itemconfig(self.team_text, fill=f'#{alpha:02x}{alpha:02x}{alpha:02x}')
            self.root.after(50, self.fade_out_intro, alpha)
        else:
            self.intro_canvas.pack_forget()
            self.setup_main_ui()

    def setup_main_ui(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
    
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        self.frame = ttk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.load_logo()
        self.create_label("Press Play to start!")
        self.create_button("Play", self.start_game)
        self.create_palette_selector()
        self.create_mute_button()

        self.root.bind("<Configure>", self.on_resize)
        self.draw_gradient()

    def load_logo(self):
        self.logo_label = ttk.Label(self.frame, image=self.logo_photo)
        self.logo_label.pack(pady=(0, 10))

    def setup_main_ui(self):
        """
        Sets up the main user interface, including the canvas, frame, logo,
        label, and button.
        Binds the resize event to the on_resize method and draws the
        initial gradient.
        """
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.canvas = Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.content_frame = ttk.Frame(self.canvas)

        self.frame = tk.Frame(self.root, bg=None)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.load_logo()
        self.create_button("Play", self.start_game)
        self.create_palette_selector()
        self.create_mute_button()

        self.root.bind("<Configure>", self.on_resize)
        self.draw_gradient()

    def draw_gradient(self):
        """
        Draws a vertical blue gradient on the canvas.
        Clears any previous gradient before drawing a new one.
        """
        height = self.root.winfo_height()
        width = self.root.winfo_width()
        self.canvas.delete("all")
        primary_color = self.color_palettes[self.selected_palette.get()]["primary"]
        secondary_color = self.color_palettes[self.selected_palette.get()]["secondary"]
        for i in range(0, height, 2):
            r1, g1, b1 = [int(primary_color[i:i+2], 16) for i in (1, 3, 5)]
            r2, g2, b2 = [int(secondary_color[i:i+2], 16) for i in (1, 3, 5)]
            r = int(r1 + (r2 - r1) * i / height)
            g = int(g1 + (g2 - g1) * i / height)
            b = int(b1 + (b2 - b1) * i / height)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def load_logo(self):
        """
        Loads and displays the logo image in the center frame.
        Uses LANCZOS for better quality image resizing.
        """
        img = Image.open(resource_path("assets/img/logo.png"))
        img = img.resize((200, 200), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(img)
        self.logo_label = Label(self.frame, image=self.logo_image)
        self.logo_label.image = self.logo_image
        self.logo_label.pack(pady=(0, 10))

    def create_label(self, text):
        """
        Creates and packs a label with the given text in the center frame.

        Args:
            text (str): The text to display in the label.
        """
        label = tk.Label(self.frame, text=text, bg=self.color_palettes[self.selected_palette.get()]["primary"], 
                         fg=self.color_palettes[self.selected_palette.get()]["accent"])
        label.pack(pady=(0, 10))

    def create_button(self, text, command):
        """
        Creates and packs a button with the given text and command in
        the center frame.

        Args:
            text (str): The text to display on the button.
            command (function): The function to call when the
            button is clicked.
        """
        button_style = ttk.Style()
        button_style.configure("TButton", 
                               background=self.color_palettes[self.selected_palette.get()]["secondary"],
                               foreground=self.color_palettes[self.selected_palette.get()]["primary"],
                               font=("Helvetica", 14),
                               padding=10)
        button_style.map("TButton", 
                         background=[('active', self.color_palettes[self.selected_palette.get()]["accent"])])
        
        button = ttk.Button(self.frame, text=text, command=command, style="TButton")
        button.pack(pady=(0, 10))

    def toggle_mute(self):
        self.is_muted.set(not self.is_muted.get())
        if self.is_muted.get():
            pygame.mixer.music.pause()
            self.mute_button.config(text="Unmute")
        else:
            pygame.mixer.music.unpause()
            self.mute_button.config(text="Mute")

    def create_palette_selector(self):
        label = ttk.Label(self.frame, text="Select Color Palette:", 
                          style="TLabel")
        label.pack(pady=(10, 5))
        self.style.configure("TMenubutton", 
                             background=self.color_palettes[self.selected_palette.get()]["secondary"],
                             foreground=self.color_palettes[self.selected_palette.get()]["primary"],
                             font=("Helvetica", 12),
                             padding=5)
        option_menu = ttk.OptionMenu(self.frame, self.selected_palette, 
                                     self.selected_palette.get(), 
                                     *self.color_palettes.keys(), 
                                     command=self.update_color_scheme,
                                     style="TMenubutton")
        option_menu.pack()

    def create_mute_button(self):
        self.style.configure("Mute.TButton", 
                             background=self.color_palettes[self.selected_palette.get()]["secondary"],
                             foreground=self.color_palettes[self.selected_palette.get()]["primary"],
                             font=("Helvetica", 12),
                             padding=5)
        
        self.mute_button = ttk.Button(self.frame, text="Mute", command=self.toggle_mute, style="Mute.TButton", padding=5,)
        self.mute_button.pack(pady=(10, 10))

    def update_color_scheme(self, *args):
        self.draw_gradient()
        for child in self.frame.winfo_children():
            widget_type = child.winfo_class()
            if widget_type == "TLabel":
                self.style.configure("TLabel", 
                                     background=self.color_palettes[self.selected_palette.get()]["primary"],
                                     foreground=self.color_palettes[self.selected_palette.get()]["accent"])
            elif widget_type in ["TButton", "TMenubutton"]:
                self.style.configure(widget_type, 
                                     background=self.color_palettes[self.selected_palette.get()]["secondary"],
                                     foreground=self.color_palettes[self.selected_palette.get()]["primary"])
                self.style.map(widget_type, 
                               background=[('active', self.color_palettes[self.selected_palette.get()]["accent"])])
        
        self.style.configure("Mute.TButton", 
                             background=self.color_palettes[self.selected_palette.get()]["secondary"],
                             foreground=self.color_palettes[self.selected_palette.get()]["primary"])
        self.style.map("Mute.TButton", 
                       background=[('active', self.color_palettes[self.selected_palette.get()]["accent"])])

    def on_resize(self, event=None):
        """
        Handles the window resize event by redrawing the gradient.

        Args:
            event (tk.Event, optional): The resize event. Defaults to None.
        """
        self.draw_gradient()

    def start_game(self):
        """
        Starts the Game of Life by destroying the current UI elements and
        initializing the GameOfLife class.
        """
        self.frame.destroy()
        self.canvas.destroy()
        self.game = GameOfLife(self.root, self.color_palettes[self.selected_palette.get()], self.is_muted)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

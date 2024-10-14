import tkinter as tk
from tkinter import Label, Canvas
from PIL import Image, ImageTk
from gol import GameOfLife
from utils import resource_path


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
        self.setup_main_ui()

    def setup_main_ui(self):
        """
        Sets up the main user interface, including the canvas, frame, logo,
        label, and button.
        Binds the resize event to the on_resize method and draws the
        initial gradient.
        """
        self.canvas = Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        self.frame = tk.Frame(self.root, bg=None)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.load_logo()
        self.create_label("Press Play to start!")
        self.create_button("Play", self.start_game)

        self.root.bind("<Configure>", self.on_resize)
        self.draw_gradient()

    def draw_gradient(self):
        """
        Draws a vertical blue gradient on the canvas.
        Clears any previous gradient before drawing a new one.
        """
        height = self.root.winfo_height()
        width = self.root.winfo_width()
        self.canvas.delete("all")  # Clear previous gradient
        for i in range(0, height, 2):  # Step by 2 for slight optimization
            b = int(i * 255 / height)
            color = f'#0000{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)

    def load_logo(self):
        """
        Loads and displays the logo image in the center frame.
        Uses LANCZOS for better quality image resizing.
        """
        img = Image.open(resource_path("assets/img/logo.jpg"))
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
        label = tk.Label(self.frame, text=text)
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
        button = tk.Button(self.frame, text=text, command=command)
        button.pack()

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
        self.game = GameOfLife(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

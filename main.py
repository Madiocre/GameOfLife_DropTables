import tkinter as tk
from tkinter import Label, Canvas
from PIL import Image, ImageTk
from gol import GameOfLife

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Of Life DropTables;")
        self.root.geometry("700x500")

        self.setup_main_ui()

    def setup_main_ui(self):
        self.canvas = Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        self.draw_gradient()

        self.frame1 = tk.Frame(self.root, bg=None)
        self.frame1.place(relx=0.5, rely=0.5, anchor="center")

        self.load_logo()

        self.label1 = tk.Label(self.frame1, text="Press Play to start!")
        self.label1.pack(pady=(0, 10))

        self.button = tk.Button(self.frame1, text="Play", command=self.start_game)
        self.button.pack()

        self.root.bind("<Configure>", self.on_resize)

    def draw_gradient(self):
        height = self.root.winfo_height()
        for i in range(0, height):
            r = 0
            g = 0
            b = int(i * 255 / height)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, self.root.winfo_width(), i, fill=color)

    def load_logo(self):
        img = Image.open("./assets/img/logo.jpg")
        img = img.resize((200, 200))
        self.logo_image = ImageTk.PhotoImage(img)

        self.logo_label = Label(self.frame1, image=self.logo_image)
        self.logo_label.image = self.logo_image
        self.logo_label.pack(pady=(0, 10))

    def on_resize(self, event):
        self.draw_gradient()

    def start_game(self):
        self.frame1.destroy()
        self.canvas.destroy()
        self.game = GameOfLife(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

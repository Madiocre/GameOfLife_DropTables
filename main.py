import sys
from os import path
import customtkinter as ctk
from PIL import Image
from gol import GameOfLife
from utils import resource_path

class MainApplication:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Game Of Life DropTables;")
        self.root.geometry("800x600")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.setup_main_ui()
        self.root.mainloop()

    def setup_main_ui(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        self.logo_image = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/img/logo_light.jpg")),
            dark_image=Image.open(resource_path("assets/img/logo_dark.jpg")),
            size=(200, 200)
        )

        self.logo_label = ctk.CTkLabel(self.main_frame, image=self.logo_image, text="")
        self.logo_label.pack(pady=(50, 20))

        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Game of Life",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))

        self.start_button = ctk.CTkButton(
            self.main_frame,
            text="Start Game",
            command=self.start_game,
            width=200,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.start_button.pack(pady=20)

        self.theme_switch = ctk.CTkSwitch(
            self.main_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.pack(pady=20)
        self.theme_switch.select()  # Start in dark mode

    def toggle_theme(self):
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def start_game(self):
        self.main_frame.pack_forget()
        self.game = GameOfLife(self.root)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
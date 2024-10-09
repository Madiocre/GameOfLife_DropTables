import tkinter as tk
from tkinter import Label, Button, Canvas
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Game Of Life DropTables;")
root.geometry("700x500")

canvas = Canvas(root)
canvas.pack(fill="both", expand=True)

# Create a bluish gradient
for i in range(0, 500):
    r = 0
    g = 0
    b = int(i * 255 / 500)
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_line(0, i, 700, i, fill=color)

# Create a frame on top of the canvas
frame1 = tk.Frame(root, bg=None)  # Set background to None
frame1.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Load and position the logo
img = Image.open("./assets/img/logo.jpg")
img = img.resize((200, 200))
logo_image = ImageTk.PhotoImage(img)

logo_label = Label(frame1, image=logo_image)
logo_label.image = logo_image
logo_label.pack(pady=(0, 10))  # Add some padding below the logo

# Add the label and button
label1 = tk.Label(frame1, text="Press Play to start!")
label1.pack(pady=(0, 10))

def on_button_click():
    label1.config(text="Button Clicked!")

button = tk.Button(frame1, text="Play", command=on_button_click)
button.pack()

root.mainloop()

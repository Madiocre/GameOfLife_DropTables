import tkinter as tk

# Step 1: Create the main window
root = tk.Tk()
root.title("Simple Tkinter App")  # Set the title of the window
root.geometry("300x200")  # Set the size of the window (width x height)

# Step 2: Add widgets (like buttons, labels, etc.)
label = tk.Label(root, text="Hello, Tkinter!")  # Create a label widget
label.pack(pady=10)  # Add padding and place the label

# Step 3: Create a button that interacts with the user
def on_button_click():
    label.config(text="Button Clicked!")

button = tk.Button(root, text="Click Me", command=on_button_click)  # Create a button widget
button.pack(pady=10)  # Place the button

# Step 4: Start the Tkinter event loop
root.mainloop()

import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter Example")
root.geometry("300x200")  # width x height

# Function to run when button is clicked
def say_hello():
    name = name_entry.get()
    message_label.config(text=f"Hello, {name}!")

# Label
greeting_label = tk.Label(root, text="Enter your name:")
greeting_label.pack(pady=10)  # Add vertical spacing

# Entry (input box)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

# Button
hello_button = tk.Button(root, text="Greet Me", command=say_hello)
hello_button.pack(pady=10)

# Label to show message
message_label = tk.Label(root, text="")
message_label.pack(pady=10)

# Run the GUI
root.mainloop()

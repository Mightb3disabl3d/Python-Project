#This is a password generator program for a school project
import secrets as s
import tkinter as tk
import string as str

root = tk.Tk()
root.title("Password Generator")
root.geometry("300x200")  # width x height

# Function to run when button is clicked
def generate_password():
    password = length_pass.get()
    message_label.config(text=f"Hello, {password}!")

# Label
length = tk.Label(root, text="Length of password")
length.pack(pady=10)  # Add vertical spacing

# Entry (input box)
length_pass = tk.Entry(root)
length_pass.pack(pady=5)

# Button
hello_button = tk.Button(root, text="Generate Password", command=generate_password)
hello_button.pack(pady=10)

# Label to show message
message_label = tk.Label(root, text="")
message_label.pack(pady=10)

# Run the GUI
root.mainloop()



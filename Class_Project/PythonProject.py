#This is a password generator program for a school project
import secrets as s
import tkinter as tk
import string as str
from tkinter import messagebox

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x400")  # width x height

# Vars:

length_var = tk.StringVar(value=12)
mixed_var = tk.BooleanVar(value=False)
num_var = tk.BooleanVar(value=False)
sym_var = tk.BooleanVar(value=False)

def validate_number(new_value):
    if new_value == "":
        return True  # allow clearing the box

    if new_value.isdigit():
        return True  # valid

    # Invalid → play system error sound
    root.bell()
    return False

vcmd = root.register(validate_number)

def generate_password(length, use_mixed, use_num, use_sym):
    characters = str.ascii_lowercase
    if use_mixed:
        characters += str.ascii_uppercase
    if use_num:
        characters += str.digits
    if use_sym:
        characters += str.punctuation

    password = ''.join(s.choice(characters) for _ in range(length))
    return password

def generate():
    length = length_var.get()
    use_mixed = mixed_var.get()
    use_num = num_var.get()
    use_sym = sym_var.get()

    if not length:
        messagebox.showerror("Error", "Please enter a password length.")
        return
    
    length = int(length)

    if length <= 0:
        messagebox.showerror("Error", "Password length must be greater than 0.")
        return
    elif length > 64:
        messagebox.showerror("Error", "Password length must be 64 or less.")
        return
    
    password = generate_password(length, use_mixed, use_num, use_sym)

    password_entry.config(state="normal")  # Enable editing temporarily
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    password_entry.config(state="readonly")  # Make it read-only

# Password length
tk.Label(root, text="Enter the desired password length:(1-64)").pack(pady=(12, 0))
length_entry = tk.Entry(
    root,
    textvariable=length_var,
    validate="key",
    validatecommand=(vcmd, "%P"),
    width=8,
    justify="center"
)
length_entry.pack(pady=5)

# Options
tk.Checkbutton(root, text="Include Symbols", variable=sym_var).pack()
tk.Checkbutton(root, text="Include Numbers", variable=num_var).pack()
tk.Checkbutton(root, text="Mixed Case", variable=mixed_var).pack()

# Generate button
tk.Button(root, text="Generate Password", command=generate).pack(pady=10)

# Password display
tk.Label(root, text="Generated Password:").pack()
password_entry = tk.Entry(root, width=30, state="readonly", justify="center")
password_entry.pack(pady=5)

# --- Run the GUI ---
root.mainloop()

    

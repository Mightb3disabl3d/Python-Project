#This is a password generator program for a school project
#Created by Ywjfeej Moua 
import secrets as s
import tkinter as tk
import string as str
from tkinter import messagebox

class PassGenerator:
    def __init__(self, root):
        self.root = root 
        self.root.title("Password Generator")
        self.root.geometry("400x400")  # width x height
        
        self.length_pass = tk.StringVar(value=10)
        self.include_upperandlower = tk.BooleanVar(value=False)
        self.include_nums = tk.BooleanVar(value=False)
        self.include_sym = tk.BooleanVar(value=False)

        validatenumtotink = self.root.register(self.valnum)

        tk.Label(root, text="Enter the desired password length:(1-64)").pack(pady=(12, 0))
        length_entry = tk.Entry(
            root,
            textvariable=self.length_pass,
            validate="key",
            validatecommand=(validatenumtotink, "%P"),
            width=8,
            justify="center"
            )
        length_entry.pack(pady=5)
        tk.Checkbutton(root, text="Include Symbols", variable=self.include_sym).pack()
        tk.Checkbutton(root, text="Include Numbers", variable=self.include_nums).pack()
        tk.Checkbutton(root, text="Mixed Case", variable=self.include_upperandlower).pack()

        # button
        tk.Button(root, text="Generate Password", command=self.generate).pack(pady=10)

        #display
        tk.Label(root, text="Generated Password:").pack()
        self.password_entry = tk.Entry(root, width=30, state="readonly", justify="center")
        self.password_entry.pack(pady=5)
    
        
    def valnum(self, value):
        if value == "":
            return True  # allow clearing the box

        if value.isdigit():
            return True  # valid

        self.root.bell()
        return False
    
    def passwordrand(self, length, use_mixed, use_num, use_sym):
        characters = str.ascii_lowercase
        if use_mixed:
            characters += str.ascii_uppercase
        if use_num:
            characters += str.digits
        if use_sym:
            characters += str.punctuation

        password = ''.join(s.choice(characters) for _ in range(length))
        return password
    
    def generate(self):
        length_text = self.length_pass.get()

        if not length_text:
            messagebox.showerror("Error", "Please enter a password length.")
            return

        length = int(length_text)

        if not (1 <= length <= 64):
            messagebox.showerror("Error", "Password length must be between 1 and 64.")
            return

        pwd = self.passwordrand(length, self.include_upperandlower.get(), self.include_nums.get(), self.include_sym.get())

        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, pwd)
        self.password_entry.config(state="readonly")

if __name__ == "__main__":
    root = tk.Tk()
    app = PassGenerator(root)
    root.mainloop()

    








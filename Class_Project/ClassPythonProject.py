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
        self.includeupperandlower = tk.BooleanVar(value=False)
        self.includenums = tk.BooleanVar(value=False)
        self.includesym = tk.BooleanVar(value=False)

        validatenumtotink = self.root.register(validate_number)

        



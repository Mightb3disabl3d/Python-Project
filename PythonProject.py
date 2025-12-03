#This is a password generator program for a school project
import secrets as s
import tkinter as tk

def generate_password():
    length = int(length_entry.get())
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
    password = ''.join(s.choice(alphabet) for _ in range(length))
    password_label.config(text=f"Generated Password: {password}")


import tkinter as tk
from tkinter import messagebox

def show_login(root, on_success):
    login_win = tk.Toplevel(root)
    login_win.title("Login")
    login_win.geometry("300x180")
    login_win.grab_set()
    login_win.resizable(False, False)

    tk.Label(login_win, text="Username:").pack(pady=(20, 5))
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password:").pack(pady=(10, 5))
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def try_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin":
            login_win.destroy()
            on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(login_win, text="Login", command=try_login).pack(pady=20)
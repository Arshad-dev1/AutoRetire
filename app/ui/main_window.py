import tkinter as tk
from tkinter import ttk

from app.ui.code_review_tab import create_code_review_tab
from app.ui.deployment_tab import create_deployment_tab
from app.ui.github_commit_tab import create_github_commit_tab
from app.ui.home_tab import create_home_tab
from app.ui.post_prod_validation_tab import create_post_prod_validation_tab
from app.ui.testing_tab import create_testing_tab

def run_app():
    root = tk.Tk()
    root.title("Auto Retire Utility Tool")
    root.geometry("1200x800")
    root.configure(bg="#ffffff")  # Set root background to white

    # Remove the following lines to eliminate the theme and style configuration
    # style = ttk.Style(root)
    # style.theme_use("default")
    # style.configure(".", background="#ffffff", foreground="#000000")
    # style.configure("TNotebook", background="#ffffff", borderwidth=0, foreground="#000000")
    # style.configure("TNotebook.Tab", background="#ffffff", foreground="#000000")
    # style.configure("TFrame", background="#ffffff")
    # style.configure("TLabelframe", background="#ffffff", foreground="#000000")
    # style.configure("TLabelframe.Label", background="#ffffff", foreground="#000000")
    # style.configure("TLabel", background="#ffffff", foreground="#000000")
    # style.configure("TEntry", fieldbackground="#ffffff", foreground="#000000")
    # style.configure("TButton", background="#ffffff", foreground="#000000")


    # bg_image = Image.open("background.jpg")
    # bg_image = bg_image.resize((500, 300), Image.ANTIALIAS)  # Resize if needed
    # bg_photo = ImageTk.PhotoImage(bg_image)
    # --- Login Frame ---
    login_frame = tk.Frame(root)
    login_frame.pack(fill=tk.BOTH, expand=True)

    # background_label = tk.Label(frame, image=bg_photo)
    # background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # background_label.lower()

    tk.Label(login_frame, text="Username:", ).pack(pady=(80, 5))
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    tk.Label(login_frame, text="Password:").pack(pady=(10, 5))
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.pack()

    def try_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin":
            login_frame.pack_forget()
            show_main_window()
        else:
            tk.messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(login_frame, text="Login", command=try_login).pack(pady=20)

    # --- Main App UI ---
    def show_main_window():
        # Top frame for logout button
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        tk.Button(top_frame, text="Logout", command=logout).pack(anchor="ne", padx=10, pady=10)

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Home Tab
        home_frame = create_home_tab(notebook)
        notebook.add(home_frame, text="Home")

        # GithubCommit Tab
        github_commit_frame = create_github_commit_tab(notebook)
        notebook.add(github_commit_frame, text="GithubCommit")

        # Code Review Tab
        code_review_frame = create_code_review_tab(notebook)
        notebook.add(code_review_frame, text="Code Review")

        # Deployment Tab
        deployment_frame = create_deployment_tab(notebook)
        notebook.add(deployment_frame, text="Deployment")

        # Testing Tab
        testing_frame = create_testing_tab(notebook)
        notebook.add(testing_frame, text="Testing")

        # Post PROD Validation Tab
        post_prod_validation_frame = create_post_prod_validation_tab(notebook)
        notebook.add(post_prod_validation_frame, text="Post PROD Validation")

        # Store references for logout
        root._main_widgets = [top_frame, notebook]

    def logout():
        # Destroy all main app widgets
        for widget in getattr(root, "_main_widgets", []):
            widget.destroy()
        login_frame.pack(fill=tk.BOTH, expand=True)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox

from app.ui.code_review_tab import create_code_review_tab
from app.ui.deployment_tab import create_deployment_tab
from app.ui.github_commit_tab import create_github_commit_tab, set_impacted_objects, set_generated_scripts
from app.ui.home_tab import create_home_tab
from app.ui.post_prod_validation_tab import create_post_prod_validation_tab
from app.ui.testing_tab import create_testing_tab


def run_app():
    root = tk.Tk()
    root.title("Auto Retire Utility Tool")
    root.geometry("1200x800")
    root.configure(bg="#f5f5f5")

    # Set ttk theme and colors
    style = ttk.Style()
    style.theme_use("default")
    style.configure(".", background="#f5f5f5", foreground="#000000")
    style.configure("TFrame", background="#f5f5f5")
    style.configure("TLabel", background="#f5f5f5", foreground="#000000")
    style.configure("TFrame.TLabel", background="#ffffff", foreground="#000000")
    style.configure("TNotebook", background="#f5f5f5")
    style.configure("TNotebook.Tab", background="#ffffff", foreground="#000000", padding=[20, 5])
    style.map("TNotebook.Tab", background=[("selected", "#e0e0e0")])
    style.configure(
        "Material.TButton",
        background="#ffffff",
        foreground="#000000",
        borderwidth=0,
        focusthickness=3,
        focuscolor="#2196F3",
        padding=(12, 8),
        relief="flat"
    )
    style.map(
        "Material.TButton",
        background=[("active", "#e0e0e0"), ("pressed", "#bbdefb")],
        relief=[("pressed", "groove"), ("!pressed", "flat")]
    )
    style.configure(
        "Material.TEntry",
        fieldbackground="#ffffff",
        foreground="#000000",
        borderwidth=2,
        relief="flat",
        padding=8
    )
    style.configure(
        "Treeview",
        background="#ffffff",
        foreground="#000000",
        fieldbackground="#ffffff",
        bordercolor="#e0e0e0",
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background="#f5f5f5",
        foreground="#000000",
        bordercolor="#e0e0e0",
        borderwidth=0
    )

    # --- Scrollable center-aligned main frame ---
    main_canvas = tk.Canvas(root, bg="#f5f5f5", highlightthickness=0)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    v_scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    main_canvas.configure(yscrollcommand=v_scrollbar.set)

    main_frame = tk.Frame(main_canvas, bg="#f5f5f5")
    canvas_window = main_canvas.create_window((0, 0), window=main_frame, anchor="n")

    def on_main_frame_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        canvas_width = event.width
        main_canvas.itemconfig(canvas_window, width=canvas_width)

    def on_canvas_resize(event):
        canvas_width = event.width
        main_canvas.itemconfig(canvas_window, width=canvas_width)

    main_frame.bind("<Configure>", on_main_frame_configure)
    main_canvas.bind("<Configure>", on_canvas_resize)

    login_frame = tk.Frame(main_frame, bg="#f5f5f5")
    login_frame.pack(pady=100)

    username_var = tk.StringVar(value="admin")
    ttk.Label(login_frame, text="Username:").pack(pady=(80, 5))
    username_entry = ttk.Entry(login_frame, textvariable=username_var, style="Material.TEntry")
    username_entry.pack()

    ttk.Label(login_frame, text="Password:").pack(pady=(10, 5))
    password_var = tk.StringVar(value="admin")
    password_entry = ttk.Entry(login_frame, show="*", textvariable=password_var, style="Material.TEntry")
    password_entry.pack()

    def logout():
        for widget in main_frame.winfo_children():
            if widget != login_frame:
                widget.destroy()
        username_var.set("")
        password_var.set("")
        username_entry.focus_set()
        login_frame.pack(pady=100)

    def try_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin":
            login_frame.pack_forget()
            show_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    ttk.Button(
        login_frame,
        text="Login",
        command=try_login,
        style="Material.TButton"
    ).pack(pady=20)

    def show_main_window():
        top_frame = ttk.Frame(main_frame, style="TFrame")
        top_frame.pack(fill=tk.X, side=tk.TOP)
        ttk.Button(top_frame, text="Logout", command=logout, style="Material.TButton").pack(anchor="ne", padx=10, pady=10)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        home_frame = create_home_tab(notebook)
        github_commit_frame = create_github_commit_tab(notebook, home_frame=home_frame)
        code_review_frame = create_code_review_tab(notebook, home_frame=home_frame)
        deployment_frame = create_deployment_tab(notebook, home_frame=home_frame)
        testing_frame = create_testing_tab(notebook, home_frame=home_frame)
        post_prod_validation_frame = create_post_prod_validation_tab(notebook, home_frame=home_frame)

        notebook.add(home_frame, text="Home")
        notebook.add(github_commit_frame, text="GithubCommit")
        notebook.add(code_review_frame, text="Code Review")
        notebook.add(testing_frame, text="Testing")
        notebook.add(deployment_frame, text="Deployment")
        notebook.add(post_prod_validation_frame, text="Post PROD Validation")

        for i in range(1, notebook.index("end")):
            notebook.tab(i, state="disabled")

        def enable_next_tab(current_index):
            if current_index + 1 < notebook.index("end"):
                notebook.tab(current_index + 1, state="normal")
                notebook.select(current_index + 1)

        frames = [
            home_frame,
            github_commit_frame,
            testing_frame,
            deployment_frame
        ]

        for idx, frame in enumerate(frames):
            def on_next(i=idx):
                if i == 0:
                    impacted_objects = []
                    for row in home_frame.row_widgets:
                        obj_type = row["object_type"].get()
                        if obj_type in ("SSRS", "SSIS") or row["selected"].get():
                            impacted_objects.append((
                                obj_type,
                                row["object_name"].get(),
                                row["server_path"].get()
                            ))
                    if not impacted_objects:
                        print("No impacted objects selected.")
                    else:
                        print(f"Impacted objects: {impacted_objects}")
                    set_impacted_objects(impacted_objects)
                    generated_scripts = getattr(home_frame, "generated_script_paths", [])
                    print(f"Generated scripts: {generated_scripts}")
                    set_generated_scripts(generated_scripts)

                if i == 1:
                    nonlocal code_review_frame
                    if code_review_frame is not None:
                        code_review_frame.destroy()
                    code_review_frame = create_code_review_tab(notebook, home_frame=home_frame)
                    if notebook.index("end") < 3 or notebook.tabs()[2] != str(code_review_frame):
                        notebook.insert(2, code_review_frame, text="Code Review")
                    else:
                        notebook.forget(2)
                        notebook.insert(2, code_review_frame, text="Code Review")

                enable_next_tab(i)

            btn = ttk.Button(frame, text="Next", command=on_next, style="Material.TButton")
            btn.pack(side=tk.BOTTOM, pady=10)

        root._main_widgets = [top_frame, notebook]

    root.mainloop()

import tkinter as tk
from tkinter import HIDDEN, ttk
from tkinter import messagebox
import os

# Shared data structure (to be updated by home_tab.py)
IMPACTED_OBJECTS = []
GENERATED_SCRIPTS = []

def set_impacted_objects(objects):
    global IMPACTED_OBJECTS
    IMPACTED_OBJECTS = objects

def set_generated_scripts(scripts):
    global GENERATED_SCRIPTS
    GENERATED_SCRIPTS = scripts
    print("Generated Scripts Set:", GENERATED_SCRIPTS)  # Debugging line

def create_github_commit_tab(notebook, home_frame=None):
    frame = ttk.Frame(notebook)

    # --- Preview Section for JIRA, Report Name, Author Email ---
    preview_frame = ttk.LabelFrame(frame, text="Submission Preview")
    preview_frame.pack(fill=tk.X, padx=10, pady=5)
    jira_label = tk.Label(preview_frame, text="JIRA #: ")
    jira_label.grid(row=0, column=0, sticky="w", padx=5)
    report_label = tk.Label(preview_frame, text="Report Name: ")
    report_label.grid(row=0, column=1, sticky="w", padx=5)
    author_label = tk.Label(preview_frame, text="Author Email: ")
    author_label.grid(row=0, column=2, sticky="w", padx=5)

    # Function to update preview labels
    def update_preview(*args):
        if home_frame:
            jira_label.config(text=f"JIRA #: {home_frame.jira_var.get()}")
            report_label.config(text=f"Report Name: {home_frame.report_name_var.get()}")
            author_label.config(text=f"Author Email: {home_frame.author_email_var.get()}")

    # If home_frame is provided, trace variables for live update
    if home_frame:
        home_frame.jira_var.trace_add("write", update_preview)
        home_frame.report_name_var.trace_add("write", update_preview)
        home_frame.author_email_var.trace_add("write", update_preview)
        update_preview()

    impacted_label = ttk.Label(frame, text="Impacted Objects Preview", font=("TkDefaultFont", 12, "bold"))
    impacted_label.pack(pady=(10, 2))

    # Table Frame
    table_frame = tk.Frame(frame)
    table_frame.pack(fill=tk.X, padx=10, pady=5)

    columns = ("", "ObjectType", "ObjectName", "Server/Path", "Github Path")
    for col_idx, col in enumerate(columns):
        tk.Label(table_frame, text=col, font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width = 2 if col == '' else 20 if col != "Server/Path" else 30).grid(row=0, column=col_idx, sticky="nsew")

    # Store checkboxes and their variables
    row_vars = []

    def refresh_table():
        # Clear previous rows (except header)
        for widget in table_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        row_vars.clear()
        row = 1
        # Add impacted objects
        for obj in IMPACTED_OBJECTS:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(table_frame, variable=var)
            cb.grid(row=row, column=0, sticky="nsew")
            tk.Label(table_frame, text=obj[0], borderwidth=0, relief="solid").grid(row=row, column=1, sticky="nsew")
            tk.Label(table_frame, text=obj[1], borderwidth=0, relief="solid").grid(row=row, column=2, sticky="nsew")
            tk.Label(table_frame, text=obj[2], borderwidth=0, relief="solid").grid(row=row, column=3, sticky="nsew")
            tk.Label(table_frame, text="toAddPath", borderwidth=0, relief="solid").grid(row=row, column=4, sticky="nsew")
            row_vars.append((var, ("object", obj)))
            row += 1
        # Add generated scripts
        for script_path in GENERATED_SCRIPTS:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(table_frame, variable=var)
            cb.grid(row=row, column=0, sticky="nsew")
            filename = os.path.basename(script_path)
            file_name = os.path.splitext(filename)[0]
            tk.Label(table_frame, text="Script", borderwidth=0, relief="solid").grid(row=row, column=1, sticky="nsew")
            tk.Label(table_frame, text=file_name, borderwidth=0, relief="solid").grid(row=row, column=2, sticky="nsew")
            tk.Label(table_frame, text=script_path, borderwidth=0, relief="solid").grid(row=row, column=3, sticky="nsew")
            tk.Label(table_frame, text="ToAddPath", borderwidth=0, relief="solid").grid(row=row, column=4, sticky="nsew")
            row_vars.append((var, ("script", script_path)))
            row += 1

    refresh_table()

   
    # --- Commit Result display section (initially hidden) ---
    commit_result_frame = tk.Frame(frame)
    commit_id_var = tk.StringVar()
    commit_id_label = tk.Label(commit_result_frame, textvariable=commit_id_var, fg="green", font=("TkDefaultFont", 10, "bold"))
    commit_id_label.pack(anchor="w", pady=(0, 5))
    # Table header for published items
    published_table_frame = tk.Frame(commit_result_frame)
    published_table_frame.pack(anchor="w")
    # Do NOT pack commit_result_frame yet; will pack after push

    def push_to_git():
        selected_objects = []
        selected_scripts = []
        for var, (typ, data) in row_vars:
            if var.get():
                if typ == "object":
                    selected_objects.append(data)
                elif typ == "script":
                    selected_scripts.append(data)
        messagebox.showinfo("Push to Git", f"Pushed to git successfully")

        # Remove selected objects from IMPACTED_OBJECTS
        global IMPACTED_OBJECTS, GENERATED_SCRIPTS
        IMPACTED_OBJECTS = [obj for obj in IMPACTED_OBJECTS if obj not in selected_objects]
        GENERATED_SCRIPTS = [script for script in GENERATED_SCRIPTS if script not in selected_scripts]
        refresh_table()

        # Show commit result section after push
        commit_id = "abc123def"  # Replace with actual commit ID from git logic
        commit_id_var.set(f"Last Commit ID: {commit_id}")

        # Clear previous published table rows
        for widget in published_table_frame.winfo_children():
            widget.destroy()

        # Table headers
        headers = ["Commit Id", "Name/Path"]
        for col, header in enumerate(headers):
            tk.Label(published_table_frame, text=header, font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=25).grid(row=0, column=col, sticky="nsew")

        row = 1
        for obj in selected_objects:
            tk.Label(published_table_frame, text="Object", borderwidth=0, relief="solid", width=25).grid(row=row, column=0, sticky="nsew")
            tk.Label(published_table_frame, text=f"{obj}", borderwidth=0, relief="solid", width=25).grid(row=row, column=1, sticky="nsew")
            row += 1
        for script in selected_scripts:
            tk.Label(published_table_frame, text="Script", borderwidth=0, relief="solid", width=25).grid(row=row, column=0, sticky="nsew")
            tk.Label(published_table_frame, text=f"{script}", borderwidth=0, relief="solid", width=25).grid(row=row, column=1, sticky="nsew")
            row += 1

        commit_result_frame.pack(pady=(0, 10), fill="x")

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=15)

    refresh_btn = tk.Button(button_frame, text="Refresh Preview", command=refresh_table)
    refresh_btn.pack(side="left", padx=5)

    push_btn = tk.Button(button_frame, text="Push to Git", command=push_to_git)
    push_btn.pack(side="left", pady=15)

     # --- Commit ID display section ---
    commit_id_var = tk.StringVar()
    commit_id_label = tk.Label(frame, textvariable=commit_id_var, fg="green", font=("TkDefaultFont", 10, "bold"))
    # Do NOT pack the label here; it will be packed after push

    def push_to_git():
        selected_objects = []
        selected_scripts = []
        for var, (typ, data) in row_vars:
            if var.get():
                if typ == "object":
                    selected_objects.append(data)
                elif typ == "script":
                    selected_scripts.append(data)
        messagebox.showinfo("Push to Git", f"Pushed to git successfully")

        # Remove selected objects from IMPACTED_OBJECTS
        global IMPACTED_OBJECTS, GENERATED_SCRIPTS
        IMPACTED_OBJECTS = [obj for obj in IMPACTED_OBJECTS if obj not in selected_objects]
        GENERATED_SCRIPTS = [script for script in GENERATED_SCRIPTS if script not in selected_scripts]
        refresh_table()

    return frame
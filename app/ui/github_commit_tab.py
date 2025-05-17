import tkinter as tk
from tkinter import HIDDEN, ttk
from tkinter import messagebox
import os

# Shared data structure (to be updated by home_tab.py)
IMPACTED_OBJECTS = []
GENERATED_SCRIPTS = []

COMMIT_RESULTS = []

def set_commit_results(results):
    global COMMIT_RESULTS
    print("Setting Commit Results:", results)  # Debugging line
    COMMIT_RESULTS = results

def get_commit_results():
    return COMMIT_RESULTS

def set_impacted_objects(objects):
    global IMPACTED_OBJECTS
    IMPACTED_OBJECTS = objects

def set_generated_scripts(scripts):
    global GENERATED_SCRIPTS
    GENERATED_SCRIPTS = scripts
    print("Generated Scripts Set:", GENERATED_SCRIPTS)  # Debugging line

def create_github_commit_tab(notebook, home_frame=None):
    frame = ttk.Frame(notebook, style="TFrame")
    frame.pack(fill=tk.BOTH, expand=True)
    frame.configure(style="TFrame")

    # --- Preview Section for JIRA, Report Name, Author Email ---
    preview_frame = ttk.LabelFrame(frame, text="Submission Preview")
    preview_frame.pack(fill=tk.X, padx=10, pady=5)
    jira_label = ttk.Label(preview_frame, text="JIRA #: ", style="TLabel")
    jira_label.grid(row=0, column=0, sticky="w", padx=5)
    report_label = ttk.Label(preview_frame, text="Report Name: ", style="TLabel")
    report_label.grid(row=0, column=1, sticky="w", padx=5)
    author_label = ttk.Label(preview_frame, text="Author Email: ", style="TLabel")
    author_label.grid(row=0, column=2, sticky="w", padx=5)

    # Function to update preview labels
    def update_preview(*args):
        if home_frame:
            jira_label.config(text=f"JIRA #: {home_frame.jira_var.get()}")
            report_label.config(text=f"Report Name: {home_frame.report_name_var.get()}")
            author_label.config(text=f"Author Email: {home_frame.author_email_var.get()}")

    if home_frame:
        home_frame.jira_var.trace_add("write", update_preview)
        home_frame.report_name_var.trace_add("write", update_preview)
        home_frame.author_email_var.trace_add("write", update_preview)
        update_preview()

    # impacted_label = ttk.Label(frame, text="Impacted Objects Preview", font=("TkDefaultFont", 12, "bold"), style="TLabel")
    # impacted_label.pack(pady=(10, 2))

    # Table Frame
    
    object_frame = ttk.LabelFrame(frame, text="Impacted Objects Preview")
    object_frame.pack(fill=tk.X, padx=10, pady=10)

    table_frame = ttk.Frame(object_frame, style="TFrame")
    table_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # Table headers
    headers = ["", "ObjectType", "ObjectName", "Server/Path", "Github Path"]
    for col_idx, header in enumerate(headers):
        ttk.Label(
            table_frame,
            text=header,
            font=("TkDefaultFont", 10, "bold"),
            borderwidth=0,
            relief="solid",
            width=2 if header == '' else 20 if header != "Server/Path" else 30,
            style="TLabel"
        ).grid(row=0, column=col_idx, sticky="nsew", padx=8, pady=6)

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
            cb = ttk.Checkbutton(table_frame, variable=var)
            cb.grid(row=row, column=0, sticky="nsew", padx=8, pady=6)
            ttk.Label(table_frame, text=obj[0], borderwidth=0, relief="solid", style="TLabel").grid(row=row, column=1, sticky="nsew", padx=8, pady=6)
            ttk.Label(table_frame, text=obj[1], borderwidth=0, relief="solid", style="TLabel").grid(row=row, column=2, sticky="nsew", padx=8, pady=6)
            ttk.Label(table_frame, text=obj[2], borderwidth=0, relief="solid", style="TLabel").grid(row=row, column=3, sticky="nsew", padx=8, pady=6)
            github_path_var = tk.StringVar(value="")
            github_path_entry = ttk.Entry(table_frame, textvariable=github_path_var, width=30, style="Material.TEntry")
            github_path_entry.grid(row=row, column=4, sticky="nsew", padx=8, pady=6)
            row_vars.append((var, ("object", obj, github_path_var)))
            row += 1
        # Add generated scripts
        for script_path in GENERATED_SCRIPTS:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(table_frame, variable=var)
            cb.grid(row=row, column=0, sticky="nsew", padx=8, pady=6)
            filename = os.path.basename(script_path)
            file_name = os.path.splitext(filename)[0]
            ttk.Label(table_frame, text="Script", borderwidth=0, relief="solid", style="TLabel").grid(row=row, column=1, sticky="nsew", padx=8, pady=6)
            ttk.Label(table_frame, text=file_name, borderwidth=0, relief="solid", style="TLabel").grid(row=row, column=2, sticky="nsew", padx=8, pady=6)
            ttk.Label(table_frame, text=script_path, borderwidth=0, relief="solid", style="TLabel").grid(row=row, column=3, sticky="nsew", padx=8, pady=6)
            github_path_var = tk.StringVar(value="")
            github_path_entry = ttk.Entry(table_frame, textvariable=github_path_var, width=30, style="Material.TEntry")
            github_path_entry.grid(row=row, column=4, sticky="nsew", padx=8, pady=6)
            row_vars.append((var, ("script", script_path, github_path_var)))
            row += 1

    refresh_table()

    # --- Commit Result display section (initially hidden) ---
    commit_result_frame = ttk.LabelFrame(frame, text="Commit Details")
    commit_result_frame.pack(fill=tk.X, padx=10, pady=10)
    commit_id_var = tk.StringVar()
    # commit_id_label = tk.Label(commit_result_frame, textvariable=commit_id_var, fg="green", font=("TkDefaultFont", 10, "bold"), bg="#ffffff")
    # commit_id_label.pack(anchor="w", pady=(0, 5))
    # Table header for published items
    published_table_frame = ttk.Frame(commit_result_frame, style="TFrame")
    published_table_frame.pack(anchor="w")
    # Do NOT pack commit_result_frame yet; will pack after push

    # Store all commit results as a list of dicts: {"commit_id": ..., "objects": [...], "scripts": [...]}
    commit_results = []

    def push_to_git():
        selected_rows = []
        for var, (typ, data, github_path_var) in row_vars:
            pr_num = "Randome Number"
            if var.get():
                github_path = github_path_var.get()
                if typ == "object":
                    # obj = (ObjectType, ObjectName, Server/Path)
                    selected_rows.append({
                        "type": "Object",
                        "name_path": data[2],
                        "artifactname": data[1],
                        "githubpath": github_path,
                        "pr_num": pr_num,
                    })
                elif typ == "script":
                    # data = script_path
                    filename = os.path.basename(data)
                    file_name = os.path.splitext(filename)[0]
                    selected_rows.append({
                        "type": "Script",
                        "name_path": data,
                        "artifactname": file_name,
                        "githubpath": github_path,
                        "pr_num": pr_num
                    })
        if not selected_rows:
            messagebox.showinfo("Push to Git", "No items selected for commit.")
            return

        # Simulate commit ID (replace with actual git logic)
        commit_id = f"commit_{len(commit_results)+1:03d}"

        # Add commit_id to each row
        for row in selected_rows:
            row["commit_id"] = commit_id

        # Add this commit to the results
        commit_results.append(selected_rows)
        # Flatten commit_results for global storage
        flat_commit_results = [item for sublist in commit_results for item in sublist]
        set_commit_results(flat_commit_results)

        messagebox.showinfo("Push to Git", f"Pushed to git successfully\nCommit ID: {commit_id}")

        # Remove selected objects/scripts from global lists
        global IMPACTED_OBJECTS, GENERATED_SCRIPTS
        IMPACTED_OBJECTS = [obj for obj in IMPACTED_OBJECTS if not any((row["type"] == "Object" and obj[2] == row["name_path"]) for row in selected_rows)]
        GENERATED_SCRIPTS = [script for script in GENERATED_SCRIPTS if not any((row["type"] == "Script" and script == row["name_path"]) for row in selected_rows)]
        refresh_table()

        # Show commit result section after push
        commit_id_var.set(f"Last Commit ID: {commit_id}")

        # Clear previous published table rows
        for widget in published_table_frame.winfo_children():
            widget.destroy()

        # Table headers
        headers = ["Commit Id", "Type", "Name/Path", "ArtifactName", "GithubPath", "PR#"]
        for col, header in enumerate(headers):
            ttk.Label(
                published_table_frame,
                text=header,
                font=("TkDefaultFont", 10, "bold"),
                borderwidth=0,
                relief="solid",
                width=15,
                style="TLabel"
            ).grid(row=0, column=col, sticky="nsew", padx=8, pady=6)

        row = 1
        # Render all commit results
        for item in flat_commit_results:
            ttk.Label(
                published_table_frame,
                text=item["commit_id"],
                borderwidth=0,
                relief="solid",
                width=25,
                style="TLabel"
            ).grid(row=row, column=0, sticky="nsew", padx=8, pady=6)
            ttk.Label(
                published_table_frame,
                text=item["type"],
                borderwidth=0,
                relief="solid",
                width=25,
                style="TLabel"
            ).grid(row=row, column=1, sticky="nsew", padx=8, pady=6)
            ttk.Label(
                published_table_frame,
                text=item["name_path"],
                borderwidth=0,
                relief="solid",
                width=25,
                style="TLabel"
            ).grid(row=row, column=2, sticky="nsew", padx=8, pady=6)
            ttk.Label(
                published_table_frame,
                text=item["artifactname"],
                borderwidth=0,
                relief="solid",
                width=25,
                style="TLabel"
            ).grid(row=row, column=3, sticky="nsew", padx=8, pady=6)
            ttk.Label(
                published_table_frame,
                text=item["githubpath"],
                borderwidth=0,
                relief="solid",
                width=25,
                style="TLabel"
            ).grid(row=row, column=4, sticky="nsew", padx=8, pady=6)
            ttk.Label(
                published_table_frame,
                text=item["pr_num"],
                borderwidth=0,
                relief="solid",
                width=25,
                style="TLabel"
            ).grid(row=row, column=5, sticky="nsew", padx=8, pady=6)
            row += 1

        commit_result_frame.pack(pady=(0, 10), fill="x", padx=10)

    button_frame = ttk.Frame(frame, style="TFrame")
    button_frame.pack(pady=15)

    refresh_btn = ttk.Button(button_frame, text="Refresh Preview", command=refresh_table, style="Material.TButton")
    refresh_btn.pack(side="left", padx=5)

    push_btn = ttk.Button(button_frame, text="Push to Git", command=push_to_git, style="Material.TButton")
    push_btn.pack(side="left", pady=15)

     # --- Commit ID display section ---
    commit_id_var = tk.StringVar()
    # commit_id_label = tk.Label(frame, textvariable=commit_id_var, fg="green", font=("TkDefaultFont", 10, "bold"))
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
        # messagebox.showinfo("Push to Git", f"Pushed to git successfully")

        # Remove selected objects from IMPACTED_OBJECTS
        global IMPACTED_OBJECTS, GENERATED_SCRIPTS
        IMPACTED_OBJECTS = [obj for obj in IMPACTED_OBJECTS if obj not in selected_objects]
        GENERATED_SCRIPTS = [script for script in GENERATED_SCRIPTS if script not in selected_scripts]
        refresh_table()

    return frame

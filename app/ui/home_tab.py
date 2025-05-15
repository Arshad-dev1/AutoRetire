import tkinter as tk
from tkinter import ttk
import webbrowser
import os

OBJECT_TYPES = [
    "Job", "Predecessor", "Successor", "Table", "Stored Procedure", "SSIS", "SSRS"
]

def open_file(filepath):
    if os.path.exists(filepath):
        webbrowser.open(f"file://{filepath}")
    else:
        folder = os.path.dirname(filepath)
        if os.path.exists(folder):
            webbrowser.open(f"file://{folder}")

def create_home_tab(notebook):
    frame = ttk.Frame(notebook)

    # Top Form Section
    form_frame = ttk.LabelFrame(frame, text="")
    form_frame.pack(fill=tk.X, padx=10, pady=10)

    # --- Store form variables for sharing ---
    frame.jira_var = tk.StringVar()
    frame.report_name_var = tk.StringVar()
    frame.author_email_var = tk.StringVar()

    tk.Label(form_frame, text="JIRA #:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
    tk.Entry(form_frame, width=15, textvariable=frame.jira_var).grid(row=0, column=1, padx=5, pady=2)
    tk.Label(form_frame, text="Report Name:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
    tk.Entry(form_frame, width=30, textvariable=frame.report_name_var).grid(row=0, column=3, padx=5, pady=2)
    tk.Label(form_frame, text="Author Email:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
    tk.Entry(form_frame, width=25, textvariable=frame.author_email_var).grid(row=0, column=5, padx=5, pady=2)

    # Impacted Objects Section (Scrollable)
    impacted_frame = ttk.LabelFrame(frame, text="Impacted Objects")
    impacted_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    # Scrollable Canvas for Impacted Objects
    impacted_canvas = tk.Canvas(impacted_frame, height=180)
    impacted_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    impacted_scrollbar = ttk.Scrollbar(impacted_frame, orient="vertical", command=impacted_canvas.yview)
    impacted_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    impacted_canvas.configure(yscrollcommand=impacted_scrollbar.set)
    impacted_canvas.bind('<Configure>', lambda e: impacted_canvas.configure(scrollregion=impacted_canvas.bbox("all")))

    rows_container = tk.Frame(impacted_canvas)
    impacted_canvas.create_window((0, 0), window=rows_container, anchor="nw")

    # Table header
    header_frame = tk.Frame(rows_container)
    header_frame.pack(fill=tk.X, padx=5, pady=2)
    tk.Label(header_frame, text="", width=3, anchor="w").grid(row=0, column=0)
    tk.Label(header_frame, text="Object Type", width=20, anchor="w").grid(row=0, column=1)
    tk.Label(header_frame, text="Object Name", width=30, anchor="w").grid(row=0, column=2)
    tk.Label(header_frame, text="Server / Path", width=40, anchor="w").grid(row=0, column=3)

    # Table body
    rows_frame = tk.Frame(rows_container)
    rows_frame.pack(fill=tk.X, padx=5, pady=2)

    # Attach row_widgets to the frame
    frame.row_widgets = []

    def on_object_type_change(var, idx, mode, row, cb):
        value = row["object_type"].get()
        if value in ("SSRS", "SSIS"):
            cb.config(state="disabled")
            row["selected"].set(False)
        else:
            cb.config(state="normal")

    def add_row(object_type="", object_name="", server_path=""):
        row = {}
        row_idx = len(frame.row_widgets)
        row["selected"] = tk.BooleanVar()
        cb = tk.Checkbutton(rows_frame, variable=row["selected"])
        cb.grid(row=row_idx, column=0, padx=2, pady=2)
        row["object_type"] = ttk.Combobox(rows_frame, values=OBJECT_TYPES, width=18)
        row["object_type"].set(object_type)
        row["object_type"].grid(row=row_idx, column=1, padx=2, pady=2)
        row["object_name"] = tk.Entry(rows_frame, width=28)
        row["object_name"].insert(0, object_name)
        row["object_name"].grid(row=row_idx, column=2, padx=2, pady=2)
        row["server_path"] = tk.Entry(rows_frame, width=38)
        row["server_path"].insert(0, server_path)
        row["server_path"].grid(row=row_idx, column=3, padx=2, pady=2)
        row["object_type"].bind("<<ComboboxSelected>>", lambda e, r=row, c=cb: on_object_type_change(None, None, None, r, c))
        if object_type in ("SSRS", "SSIS"):
            cb.config(state="disabled")
        frame.row_widgets.append(row)

    # Add initial 1 empty row
    for _ in range(1):
        add_row()

    add_btn = tk.Button(impacted_frame, text="Add", command=add_row)
    add_btn.pack(anchor="e", padx=10, pady=5)

    def fill_impacted_objects():
        for widget in rows_frame.winfo_children():
            widget.destroy()
        frame.row_widgets.clear()
        sample_data = [
            ("Job", "JobA", "/server/jobA"),
            ("Table", "TableB", "/server/tableB"),
            ("SSRS", "Report1", "/server/report1"),
            ("SSIS", "Package1", "/server/package1"),
            ("Stored Procedure", "Proc1", "/server/proc1"),
        ]
        for obj_type, obj_name, srv_path in sample_data:
            add_row(obj_type, obj_name, srv_path)

    get_impacted_btn = tk.Button(form_frame, text="Get ImpactedObjects", command=fill_impacted_objects)
    get_impacted_btn.grid(row=0, column=6, padx=10, pady=2)

    # Generate Scripts Button (above Generated Scripts)
    def update_scripts_table(new_data):
        for widget in script_links_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        for idx, (sn, file_path) in enumerate(new_data, start=1):
            tk.Label(script_links_frame, text=sn, width=8, anchor="w").grid(row=idx, column=0, sticky="w")
            link = tk.Label(script_links_frame, text=file_path, fg="blue", cursor="hand2", width=120, anchor="w")
            link.grid(row=idx, column=1, sticky="w")
            link.bind("<Button-1>", lambda e, fp=file_path: open_file(fp))

    def generate_scripts():
        new_script_data = [
            ("1", "/path/to/generated_script1.sql"),
            ("2", "/path/to/generated_script2.sql"),
            ("3", "/path/to/generated_script3.sql"),
        ]
        update_scripts_table(new_script_data)
        # Store the script paths on the frame for access in main_window
        frame.generated_script_paths = [file_path for _, file_path in new_script_data]

    generate_btn = tk.Button(frame, text="Generate Scripts", command=generate_scripts)
    generate_btn.pack(padx=10, pady=5)

    # Generated Scripts Section (Scrollable)
    scripts_frame = ttk.LabelFrame(frame, text="Generated Scripts")
    scripts_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

    scripts_canvas = tk.Canvas(scripts_frame, height=150)
    scripts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scripts_scrollbar = ttk.Scrollbar(scripts_frame, orient="vertical", command=scripts_canvas.yview)
    scripts_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Define script_links_frame within the function scope
    script_links_frame = tk.Frame(scripts_canvas)
    scripts_canvas.create_window((0, 0), window=script_links_frame, anchor="nw")
    print(f"Script links frame: {script_links_frame.__getattribute__}")  # Debugging line


    return frame
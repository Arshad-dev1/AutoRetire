import tkinter as tk
from tkinter import ttk

def create_testing_tab(notebook, home_frame=None):
    frame = ttk.Frame(notebook)
    preview_frame = ttk.LabelFrame(frame, text="Submission Preview")
    preview_frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
    jira_label = ttk.Label(preview_frame, text="JIRA #: ", style="TLabel")
    jira_label.grid(row=0, column=0, sticky="w", padx=5)
    report_label = ttk.Label(preview_frame, text="Report Name: ", style="TLabel")
    report_label.grid(row=0, column=3, sticky="w", padx=5)
    author_label = ttk.Label(preview_frame, text="Author Email: ", style="TLabel")
    author_label.grid(row=0, column=6, sticky="w", padx=5)

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

    ttk.Label(frame, text="Environment", style="TLabel").grid(row=2, column=1, sticky="ew", padx=5, pady=2)
    env_var = tk.StringVar(value="UAT/DEV")
    env_entry = ttk.Combobox(frame, textvariable=env_var, values=["UAT/DEV", "Prod", "QA"], width=15, state="readonly", style="Material.TCombobox")
    env_entry.grid(row=2, column=2, sticky="ew", padx=5, pady=2)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    # Test Details Section
    test_button = ttk.Button(frame, text="Test", style="Material.TButton", width=5)
    test_button.grid(row=3, column=1, sticky="ew", padx=5, pady=(5))

    test_details_frame = ttk.LabelFrame(frame, text="Test Details")
    test_details_frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_columnconfigure(0, weight=1)
    test_details_frame.grid(row=4, column=0, columnspan=5, sticky="ew", padx=10, pady=5)

    ttk.Label(test_details_frame, text="Overall Status :", style="TLabel").grid(row=0, column=1, sticky="e", padx=5, pady=2)
    status_var = tk.StringVar(value="Pass/Fail")
    status_entry = ttk.Entry(test_details_frame, textvariable=status_var, width=10, style="Material.TEntry")
    status_entry.grid(row=0, column=2, sticky="w", padx=5, pady=2)

    # --- Table with Scrollbar ---
    table_canvas = tk.Canvas(test_details_frame,  highlightthickness=0, bg="#f5f5f5", bd=0, height=200)
    table_scrollbar = ttk.Scrollbar(test_details_frame, orient="vertical", command=table_canvas.yview)
    table_canvas.configure(yscrollcommand=table_scrollbar.set)
    # table_canvas.pack(side="left", fill="both", expand=True, pady=5, padx=5, ipady=5, ipadx=5)
    # Assuming parent uses grid
    test_details_frame.grid_rowconfigure(2, weight=1)
    for col in range(6):  # 5 columns for table, 1 for scrollbar
        test_details_frame.grid_columnconfigure(col, weight=1)

    table_canvas.grid(row=2, column=0, columnspan=5, sticky="nsew")
    table_scrollbar.grid(row=2, column=5, sticky="ns")
    # table_scrollbar.pack(side="right", fill="y")


    table_frame = ttk.Frame(table_canvas, style="TFrame")
    table_canvas.create_window((0, 0), window=table_frame, anchor="nw")

    def on_frame_configure(event):
        table_canvas.configure(scrollregion=table_canvas.bbox("all"))

    table_frame.bind("<Configure>", on_frame_configure)

    table_headers = ["Test Step No.", "Test Step Description", "Action Procedure", "Actual Results", "Status"]
    for idx, header in enumerate(table_headers):
        ttk.Label(table_frame, text=header, font=("TkDefaultFont", 10, "bold"), width=20, style="TLabel").grid(
            row=0, column=idx, sticky="nsew", padx=8, pady=6
        )
    for col in range(len(table_headers)):
        table_frame.grid_columnconfigure(col, weight=1)

    step_rows = []

    def retrieve_test_details():
        status_var.set("Pass")
        sample_steps = [
            ("1", "Login to system", "Enter credentials", "Login successful", "Pass"),
            ("2", "Navigate to dashboard", "Click dashboard tab", "Dashboard loaded", "Pass"),
            ("3", "Run report", "Click run report", "Report generated", "Pass")
        ]
        for i, step in enumerate(sample_steps):
            if i < len(step_rows):
                for j, val in enumerate(step):
                    entry_widget = step_rows[i][j]
                    entry_widget.grid_forget()
                    label = ttk.Label(table_frame, text=val, width=20, style="TLabel")
                    label.grid(row=1 + i, column=j, sticky="nsew", padx=8, pady=6)
                    step_rows[i][j] = label
            else:
                row_entries = []
                for j, val in enumerate(step):
                    label = ttk.Label(table_frame, text=val, width=20, style="TLabel")
                    label.grid(row=1 + i, column=j, sticky="nsew", padx=8, pady=6)
                    row_entries.append(label)
                step_rows.append(row_entries)

    test_button.config(command=retrieve_test_details)

    def add_step_row():
        i = len(step_rows)
        row_entries = []
        for j in range(5):
            entry = ttk.Entry(table_frame, width=20, style="Material.TEntry")
            entry.grid(row=1 + i, column=j, sticky="nsew", padx=1, pady=1)
            row_entries.append(entry)
        step_rows.append(row_entries)

    def on_next():
        if notebook:
            idx = notebook.index(frame)
            if idx + 1 < notebook.index("end"):
                notebook.tab(idx + 1, state="normal")
                notebook.select(idx + 1)

    next_btn = ttk.Button(frame, text="Next", command=on_next, style="Material.TButton")
    next_btn.grid(row=7 + len(step_rows), column=0, columnspan=5, pady=10)

    return frame

import tkinter as tk
from tkinter import ttk

def create_testing_tab(notebook, home_frame=None):
    frame = ttk.Frame(notebook)
    preview_frame = ttk.LabelFrame(frame, text="Submission Preview")
    # preview_frame.pack(fill=tk.X, padx=10, pady=5)
    preview_frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
    jira_label = tk.Label(preview_frame, text="JIRA #: ")
    jira_label.grid(row=0, column=0, sticky="w", padx=5)
    report_label = tk.Label(preview_frame, text="Report Name: ")
    report_label.grid(row=0, column=3, sticky="w", padx=5)
    author_label = tk.Label(preview_frame, text="Author Email: ")
    author_label.grid(row=0, column=6, sticky="w", padx=5)

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

    # --- Title ---
    title_label = tk.Label(frame, text="Testing Page", font=("TkDefaultFont", 12, "bold"))
    title_label.grid(row=1, column=1, columnspan=3, pady=(10, 5), sticky="w")

    # --- Environment ---
    tk.Label(frame, text="Environment").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    env_var = tk.StringVar(value="UAT/DEV")
    env_entry = tk.Entry(frame, textvariable=env_var, width=15)
    env_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)

    # --- Test Section Header ---
    def retrieve_test_details():
        # Example: Populate fields with dummy data (replace with real retrieval logic)
        test_details_var.set("Sample test details loaded.")
        status_var.set("Pass")
        sample_steps = [
            ("1", "Login to system", "Enter credentials", "Login successful", "Pass"),
            ("2", "Navigate to dashboard", "Click dashboard tab", "Dashboard loaded", "Pass"),
            ("3", "Run report", "Click run report", "Report generated", "Pass")
        ]
        for i, step in enumerate(sample_steps):
            if i < len(step_rows):
                for j, val in enumerate(step):
                    step_rows[i][j].delete(0, tk.END)
                    step_rows[i][j].insert(0, val)
            else:
                row_entries = []
                for j, val in enumerate(step):
                    entry = tk.Entry(frame, width=20)
                    entry.grid(row=7 + i, column=j, sticky="nsew", padx=1, pady=1)
                    entry.insert(0, val)
                    row_entries.append(entry)
                step_rows.append(row_entries)

    test_button = tk.Button(frame, text="Test", font=("TkDefaultFont", 10, "bold"), bg="#e0e0e0", command=retrieve_test_details)
    test_button.grid(row=3, column=1, columnspan=3, sticky="ew", padx=5, pady=(10, 5))

    # --- Test Details ---
    tk.Label(frame, text="Test Details :").grid(row=4, column=0, sticky="e", padx=5, pady=2)
    test_details_var = tk.StringVar()
    test_details_entry = tk.Entry(frame, textvariable=test_details_var, width=40)
    test_details_entry.grid(row=4, column=1, columnspan=3, sticky="w", padx=5, pady=2)

    # --- Overall Status ---
    tk.Label(frame, text="Overall Status :").grid(row=5, column=0, sticky="e", padx=5, pady=2)
    status_var = tk.StringVar(value="Pass/Fail")
    status_entry = tk.Entry(frame, textvariable=status_var, width=10)
    status_entry.grid(row=5, column=1, sticky="w", padx=5, pady=2)

    # --- Test Steps Table Header ---
    table_headers = ["Test Step No.", "Test Step Description", "Action Procedure", "Actual Results", "Status"]
    for idx, header in enumerate(table_headers):
        tk.Label(frame, text=header, font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=6, column=idx, sticky="nsew", padx=1, pady=1)

    # --- Test Steps Rows ---
    step_rows = []
    for i in range(3):
        row_entries = []
        for j in range(5):
            entry = tk.Entry(frame, width=20)
            entry.grid(row=7 + i, column=j, sticky="nsew", padx=1, pady=1)
            row_entries.append(entry)
        step_rows.append(row_entries)

    # --- Add Row Button ---
    def add_step_row():
        i = len(step_rows)
        row_entries = []
        for j in range(5):
            entry = tk.Entry(frame, width=20)
            entry.grid(row=7 + i, column=j, sticky="nsew", padx=1, pady=1)
            row_entries.append(entry)
        step_rows.append(row_entries)

   

    # --- Next Button to go to Deployment Tab ---
    def on_next():
        # Optionally, collect and store test step data here
        if notebook:
            idx = notebook.index(frame)
            if idx + 1 < notebook.index("end"):
                notebook.tab(idx + 1, state="normal")
                notebook.select(idx + 1)

    next_btn = tk.Button(frame, text="Next", command=on_next)
    next_btn.grid(row=7 + len(step_rows), column=0, columnspan=5, pady=10)

    return frame
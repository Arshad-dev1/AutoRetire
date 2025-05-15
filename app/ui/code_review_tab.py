import tkinter as tk
from tkinter import ttk

def create_code_review_tab(notebook, home_frame=None):
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

    # Add Code Review tab UI components here
    return frame
import tkinter as tk
from tkinter import ttk

def create_deployment_tab(notebook, home_frame=None):
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

    # --- Header ---
    header = tk.Label(frame, text="Deployment Page", font=("TkDefaultFont", 12, "bold"), bg="#d9d9d9")
    header.pack(fill=tk.X, padx=10, pady=(10, 5))

    # --- Artifact Details (GitHub) Section ---
    artifact_section = ttk.LabelFrame(frame, text="Artifact Details (Github):")
    artifact_section.pack(fill=tk.X, padx=10, pady=5)

    # Table headers
    artifact_headers = ["Sno.", "Artifact Name", "Commit ID", "GitHub Path", "TFS Path"]
    for col, header_text in enumerate(artifact_headers):
        tk.Label(artifact_section, text=header_text, font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=18).grid(row=0, column=col, sticky="nsew")

    # Example row (replace with actual data fetching from GitHub Commit tab)
    tk.Label(artifact_section, text="1", borderwidth=1, relief="solid").grid(row=1, column=0, sticky="nsew")
    tk.Label(artifact_section, text="From the commit page", borderwidth=1, relief="solid").grid(row=1, column=1, sticky="nsew")
    tk.Label(artifact_section, text="From the commit page", borderwidth=1, relief="solid").grid(row=1, column=2, sticky="nsew")
    tk.Label(artifact_section, text="From the commit page", borderwidth=1, relief="solid").grid(row=1, column=3, sticky="nsew")
    tk.Label(artifact_section, text="Free text", borderwidth=1, relief="solid").grid(row=1, column=4, sticky="nsew")

    # --- TFS Check-in/Deploy Section ---
    tfs_checkin_frame = tk.Frame(frame)
    tfs_checkin_frame.pack(fill=tk.X, padx=10, pady=(15, 5))
    tfs_checkin_label = tk.Label(tfs_checkin_frame, text="TFS Check-in / Deploy", font=("TkDefaultFont", 10, "bold"), bg="#d9d9d9")
    tfs_checkin_label.pack(fill=tk.X)

    # --- TFS Artifacts Section ---
    tfs_artifact_section = ttk.LabelFrame(frame, text="TFS Artifacts:")
    tfs_artifact_section.pack(fill=tk.X, padx=10, pady=5)

    tfs_headers = ["Pipeline", "Build Number", "Build Status", "Release URL", "UAT Deployment"]
    for col, header_text in enumerate(tfs_headers):
        tk.Label(tfs_artifact_section, text=header_text, font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=18).grid(row=0, column=col, sticky="nsew")

    # Example row (replace with actual data fetching)
    for col in range(len(tfs_headers)):
        tk.Label(tfs_artifact_section, text="", borderwidth=1, relief="solid").grid(row=1, column=col, sticky="nsew")

    
    return frame
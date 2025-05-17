import tkinter as tk
from tkinter import ttk
from app.ui.github_commit_tab import get_commit_results

def create_deployment_tab(notebook, home_frame=None):
    frame = ttk.Frame(notebook)
    # --- Preview Section for JIRA, Report Name, Author Email ---
    preview_frame = ttk.LabelFrame(frame, text="Submission Preview")
    preview_frame.pack(fill=tk.X, padx=10, pady=5)
    jira_label = ttk.Label(preview_frame, text="JIRA #: ", style="TLabel")
    jira_label.grid(row=0, column=0, sticky="w", padx=5)
    report_label = ttk.Label(preview_frame, text="Report Name: ", style="TLabel")
    report_label.grid(row=0, column=1, sticky="w", padx=5)
    author_label = ttk.Label(preview_frame, text="Author Email: ", style="TLabel")
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

    # --- Artifact Details (GitHub) Section ---
    artifact_section = ttk.LabelFrame(frame, text="Artifact Details (Github):")
    artifact_section.pack(fill=tk.X, padx=10, pady=5)

    # Table headers
    artifact_headers = ["Sno.", "Artifact Name", "Commit ID", "GitHub Path", "TFS Path"]
    for col, header_text in enumerate(artifact_headers):
        ttk.Label(artifact_section, text=header_text, font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=18).grid(row=0, column=col, sticky="nsew", padx=8, pady=6)

    tfs_path_entries = []

    def refresh_artifact_section():
        # Clear previous artifact rows (except header)
        for widget in artifact_section.winfo_children():
            info = widget.grid_info()
            if info.get("row", 0) > 0:
                widget.destroy()
        tfs_path_entries.clear()
        # Fetch commit results from github_commit_tab (flat list of dicts)
        commit_results = get_commit_results()
        row_num = 1
        for item in commit_results:
            artifact_name = item.get("artifactname", "")
            commit_id = item.get("commit_id", "")
            github_path = item.get("githubpath", "")
            ttk.Label(artifact_section, text=str(row_num), borderwidth=0, relief="solid", style="TLabel").grid(row=row_num, column=0, sticky="nsew", padx=8, pady=6)
            ttk.Label(artifact_section, text=artifact_name, borderwidth=0, relief="solid", style="TLabel").grid(row=row_num, column=1, sticky="nsew", padx=8, pady=6)
            ttk.Label(artifact_section, text=commit_id, borderwidth=0, relief="solid", style="TLabel").grid(row=row_num, column=2, sticky="nsew", padx=8, pady=6)
            ttk.Label(artifact_section, text=github_path, borderwidth=0, relief="solid", style="TLabel").grid(row=row_num, column=3, sticky="nsew", padx=8, pady=6)
            tfs_entry = ttk.Entry(artifact_section, style="Material.TEntry")
            tfs_entry.grid(row=row_num, column=4, sticky="nsew", padx=8, pady=6)
            tfs_path_entries.append(tfs_entry)
            row_num += 1

    # Call refresh on load
    refresh_artifact_section()

    # Bind refresh to tab change event
    def on_tab_changed(event):
        if notebook.select() == str(frame):
            refresh_artifact_section()

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # --- TFS Check-in/Deploy Section ---
    tfs_checkin_frame = ttk.Frame(frame)
    tfs_checkin_frame.pack(fill=tk.X, padx=10, pady=(15, 5))

    def populate_tfs_artifacts():
        # Read TFS Path values from entry widgets
        tfs_paths = [entry.get() for entry in tfs_path_entries]
        # Example data to populate the TFS Artifacts table
        example_data = [
            "Pipeline-1",
            "Build-123",
            "Success",
            "http://release-url",
            "Deployed"
        ]
        # You can now use tfs_paths as needed, for example print or store them
        print("TFS Paths entered:", tfs_paths)
        for col, value in enumerate(example_data):
            tfs_artifact_section.grid_slaves(row=1, column=col)[0].config(text=value)

    tfs_checkin_btn = ttk.Button(
        frame,
        text="TFS Check-in / Deploy",
        style="Material.TButton",
        command=populate_tfs_artifacts
    )
    tfs_checkin_btn.pack(pady=(10, 2))

    # --- TFS Artifacts Section ---
    tfs_artifact_section = ttk.LabelFrame(frame, text="TFS Artifacts:")
    tfs_artifact_section.pack(fill=tk.X, padx=10, pady=(10,5))

    tfs_headers = ["Pipeline", "Build Number", "Build Status", "Release URL", "UAT Deployment"]
    for col, header_text in enumerate(tfs_headers):
        ttk.Label(tfs_artifact_section, text=header_text,style="TLabel", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=18).grid(row=0, column=col, sticky="nsew", padx=8, pady=6)

    # Example row (replace with actual data fetching)
    for col in range(len(tfs_headers)):
        ttk.Label(tfs_artifact_section, text="", borderwidth=0, relief="solid", style="TLabel").grid(row=1, column=col, sticky="nsew", padx=8, pady=6)

    return frame
import tkinter as tk
from tkinter import ttk
from app.ui.github_commit_tab import get_commit_results

def create_code_review_tab(notebook, home_frame=None, shared_data=None):
    # Use shared_data to access all previous tab data
    # e.g., shared_data["commit_results"], shared_data["review_statuses"], etc.
    frame = ttk.Frame(notebook, style="TFrame")

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

    # Set preview labels immediately if home_frame is provided
    if home_frame:
        update_preview()
        home_frame.jira_var.trace_add("write", update_preview)
        home_frame.report_name_var.trace_add("write", update_preview)
        home_frame.author_email_var.trace_add("write", update_preview)

    # --- Commit Table Section ---
    commit_table_frame = ttk.Frame(frame, style="TFrame")
    commit_table_frame.pack(fill=tk.X, padx=10, pady=5)

    # Table headers
    ttk.Label(commit_table_frame, text="Commit Id", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=20, style="TLabel").grid(row=0, column=0, sticky="nsew", padx=8, pady=6)
    ttk.Label(commit_table_frame, text="Type", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=10, style="TLabel").grid(row=0, column=1, sticky="nsew", padx=8, pady=6)
    ttk.Label(commit_table_frame, text="Github Path", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=40, style="TLabel").grid(row=0, column=2, sticky="nsew", padx=8, pady=6)
    ttk.Label(commit_table_frame, text="PR#", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=40, style="TLabel").grid(row=0, column=2, sticky="nsew", padx=8, pady=6)

    commit_results = get_commit_results()
    print("Commit Results", commit_results)
    row = 1
    for item in commit_results:
        commit_id = item.get("commit_id", "")
        typ = item.get("type", "")
        githu_path = item.get("githubpath", "")
        ttk.Label(commit_table_frame, text=commit_id, borderwidth=0, relief="solid", width=20, style="TLabel").grid(row=row, column=0, sticky="nsew", padx=8, pady=6)
        ttk.Label(commit_table_frame, text=typ, borderwidth=0, relief="solid", width=10, style="TLabel").grid(row=row, column=1, sticky="nsew", padx=8, pady=6)
        ttk.Label(commit_table_frame, text=githu_path, borderwidth=0, relief="solid", width=40, anchor="w", style="TLabel").grid(row=row, column=2, sticky="nsew", padx=8, pady=6)
        row += 1

    # --- Code Review Section ---
    def populate_review_details():
        status_var.set("Pass")
        sample_reviews = [
            ("Object1", "Pass", "Looks good"),
            ("Object2", "Fail", "Needs changes"),
            ("Script1", "Pass", "No issues")
        ]
        for i, review in enumerate(sample_reviews):
            if i < len(review_entries):
                # Remove the combobox and entry, replace with labels
                obj_name, status_entry, comment_entry = review_entries[i]
                # Remove widgets from grid
                # status_entry.grid_forget()
                # comment_entry.grid_forget()
                # Create and place labels
                status_label = ttk.Label(review_table_frame, text=review[1], width=8, style="TLabel")
                status_label.grid(row=i+1, column=2, sticky="nsew", padx=8, pady=6)
                comment_label = ttk.Label(review_table_frame, text=review[2], width=30, style="TLabel")
                comment_label.grid(row=i+1, column=3, sticky="nsew", padx=8, pady=6)
                # Update the tuple to hold labels instead of entry widgets
                review_entries[i] = (obj_name, status_label, comment_label)
        # If there are more review_entries than sample_reviews, disable the rest
        for i in range(len(sample_reviews), len(review_entries)):
            obj_name, status_entry, comment_entry = review_entries[i]
            status_entry.config(state="disabled")
            comment_entry.config(state="disabled")

    review_button = ttk.Button(frame, text="Code Review", style="Material.TButton", command=populate_review_details)
    review_button.pack(pady=(10, 2))

    review_section = ttk.LabelFrame(frame, text="Review Details")
    review_section.pack(fill=tk.X, padx=10, pady=10)

    # Overall Status
    ttk.Label(review_section, text="Overall Status:", style="TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    status_var = tk.StringVar(value="Pass")
    status_dropdown = ttk.Combobox(review_section, textvariable=status_var, values=["Pass", "Fail"], state="readonly", width=10, style="Material.TCombobox")
    status_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=2)

    # --- Review Table Section ---
    review_table_frame = ttk.Frame(review_section, style="TFrame")
    # review_table_frame.pack(fill=tk.X, padx=10, pady=10)
    review_table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    # Table headers
    ttk.Label(review_table_frame, text="S.No", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=5, style="TLabel").grid(row=0, column=0, sticky="nsew", padx=8, pady=6)
    ttk.Label(review_table_frame, text="ObjectName", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=25, style="TLabel").grid(row=0, column=1, sticky="nsew", padx=8, pady=6)
    ttk.Label(review_table_frame, text="Status", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=10, style="TLabel").grid(row=0, column=2, sticky="nsew", padx=8, pady=6)
    ttk.Label(review_table_frame, text="Comments", font=("TkDefaultFont", 10, "bold"), borderwidth=0, relief="solid", width=30, style="TLabel").grid(row=0, column=3, sticky="nsew", padx=8, pady=6)

    # Populate review table with objects/scripts from all commits
    review_row = 1
    review_entries = []
    for obj in commit_results:
        object_name = obj.get("artifactname", "")
        ttk.Label(review_table_frame, text=str(review_row), borderwidth=0, relief="solid", width=5, style="TLabel").grid(row=review_row, column=0, sticky="nsew", padx=8, pady=6)
        ttk.Label(review_table_frame, text=str(object_name), borderwidth=0, relief="solid", width=25, anchor="w", style="TLabel").grid(row=review_row, column=1, sticky="nsew", padx=8, pady=6)
        ttk.Label(review_table_frame, text="", borderwidth=0, relief="solid", width=5, style="TLabel").grid(row=review_row, column=0, sticky="nsew", padx=8, pady=6)
        ttk.Label(review_table_frame, text="", borderwidth=0, relief="solid", width=5, style="TLabel").grid(row=review_row, column=0, sticky="nsew", padx=8, pady=6)
        review_entries.append((object_name, "", ""))
        review_row += 1

    def on_next():
        # Collect review details and statuses
        # overall_status = status_var.get()
        # review_results = []
        # for obj_name, status_entry, comment_entry in review_entries:
        #     status = status_entry.get()
        #     comment = comment_entry.get()
        #     review_results.append({"object": obj_name, "status": status, "comment": comment})
        # # Optionally, store in shared_data or global for deployment tab
        # if shared_data is not None:
        #     shared_data["overall_status"] = overall_status
        #     shared_data["review_results"] = review_results
        # Move to next tab (deployment)
        if notebook:
            idx = notebook.index(frame)
            if idx + 1 < notebook.index("end"):
                notebook.tab(idx + 1, state="normal")
                notebook.select(idx + 1)

    next_btn = ttk.Button(frame, text="Next", command=on_next, style="Material.TButton")
    next_btn.pack(side=tk.BOTTOM, pady=10)

    return frame
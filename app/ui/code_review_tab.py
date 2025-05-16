import tkinter as tk
from tkinter import ttk
from app.ui.github_commit_tab import get_commit_results

def create_code_review_tab(notebook, home_frame=None, shared_data=None):
    # Use shared_data to access all previous tab data
    # e.g., shared_data["commit_results"], shared_data["review_statuses"], etc.
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

    # Set preview labels immediately if home_frame is provided
    if home_frame:
        update_preview()
        home_frame.jira_var.trace_add("write", update_preview)
        home_frame.report_name_var.trace_add("write", update_preview)
        home_frame.author_email_var.trace_add("write", update_preview)

    # --- Code Review Page Title ---
    title_label = tk.Label(frame, text="Code Review Page", font=("TkDefaultFont", 12, "bold"))
    title_label.pack(pady=(10, 2))

    # --- Commit Table Section ---
    commit_table_frame = tk.Frame(frame)
    commit_table_frame.pack(fill=tk.X, padx=10, pady=5)

    # Table headers
    tk.Label(commit_table_frame, text="Commit Id", font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=0, sticky="nsew")
    tk.Label(commit_table_frame, text="Type", font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=10).grid(row=0, column=1, sticky="nsew")
    tk.Label(commit_table_frame, text="Name/Path", font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=40).grid(row=0, column=2, sticky="nsew")

    commit_results = get_commit_results()
    print("Commit Results",commit_results);
    row = 1
    for commit in commit_results:
        commit_id = commit["commit_id"]
        for obj in commit["objects"]:
            tk.Label(commit_table_frame, text=commit_id, borderwidth=0, relief="solid", width=20).grid(row=row, column=0, sticky="nsew")
            tk.Label(commit_table_frame, text="Object", borderwidth=0, relief="solid", width=10).grid(row=row, column=1, sticky="nsew")
            tk.Label(commit_table_frame, text=obj[2], borderwidth=0, relief="solid", width=40, anchor="w").grid(row=row, column=2, sticky="nsew")
            row += 1
        for script in commit["scripts"]:
            tk.Label(commit_table_frame, text=commit_id, borderwidth=0, relief="solid", width=20).grid(row=row, column=0, sticky="nsew")
            tk.Label(commit_table_frame, text="Script", borderwidth=0, relief="solid", width=10).grid(row=row, column=1, sticky="nsew")
            tk.Label(commit_table_frame, text=str(script), borderwidth=0, relief="solid", width=40, anchor="w").grid(row=row, column=2, sticky="nsew")
            row += 1

    # --- Code Review Section ---
    def populate_review_details():
        review_details_text.delete("1.0", tk.END)
        review_details_text.insert(tk.END, "Sample review details loaded.")
        status_var.set("Pass")
        sample_reviews = [
            ("Object1", "Pass", "Looks good"),
            ("Object2", "Fail", "Needs changes"),
            ("Script1", "Pass", "No issues")
        ]
        for i, review in enumerate(sample_reviews):
            if i < len(review_entries):
                review_entries[i][1].set(review[1])
                review_entries[i][2].delete(0, tk.END)
                review_entries[i][2].insert(0, review[2])

    review_button = tk.Button(frame, text="Code Review", font=("TkDefaultFont", 10, "bold"), bg="#e0e0e0", command=populate_review_details)
    review_button.pack(pady=(10, 2))
    
    review_section = tk.LabelFrame(frame, text="Code Review")
    review_section.pack(fill=tk.X, padx=10, pady=10)
    # Review Details
    tk.Label(review_section, text="Review Details:").grid(row=0, column=0, sticky="nw", padx=5, pady=2)
    review_details_text = tk.Text(review_section, height=3, width=60)
    review_details_text.grid(row=0, column=1, sticky="w", padx=5, pady=2)

    # Overall Status
    tk.Label(review_section, text="Overall Status:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    status_var = tk.StringVar(value="Pass")
    status_dropdown = ttk.Combobox(review_section, textvariable=status_var, values=["Pass", "Fail"], state="readonly", width=10)
    status_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=2)

    # --- Review Table Section ---
    review_table_frame = tk.Frame(frame)
    review_table_frame.pack(fill=tk.X, padx=10, pady=10)

    # Table headers
    tk.Label(review_table_frame, text="S.No", font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=5).grid(row=0, column=0, sticky="nsew")
    tk.Label(review_table_frame, text="ObjectName", font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=25).grid(row=0, column=1, sticky="nsew")
    tk.Label(review_table_frame, text="Status", font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=10).grid(row=0, column=2, sticky="nsew")
    tk.Label(review_table_frame, text="Comments", font=("TkDefaultFont", 10, "bold"), borderwidth=1, relief="solid", width=30).grid(row=0, column=3, sticky="nsew")

    # Populate review table with objects/scripts from all commits
    review_row = 1
    review_entries = []
    for commit in commit_results:
        for obj in commit["objects"]:
            tk.Label(review_table_frame, text=str(review_row), borderwidth=0, relief="solid", width=5).grid(row=review_row, column=0, sticky="nsew")
            tk.Label(review_table_frame, text=obj[2], borderwidth=0, relief="solid", width=25, anchor="w").grid(row=review_row, column=1, sticky="nsew")
            status_entry = ttk.Combobox(review_table_frame, values=["Pass", "Fail"], width=8, state="readonly")
            status_entry.grid(row=review_row, column=2, sticky="nsew")
            comment_entry = tk.Entry(review_table_frame, width=30)
            comment_entry.grid(row=review_row, column=3, sticky="nsew")
            review_entries.append((obj[2], status_entry, comment_entry))
            review_row += 1
        for script in commit["scripts"]:
            tk.Label(review_table_frame, text=str(review_row), borderwidth=0, relief="solid", width=5).grid(row=review_row, column=0, sticky="nsew")
            tk.Label(review_table_frame, text=str(script), borderwidth=0, relief="solid", width=25, anchor="w").grid(row=review_row, column=1, sticky="nsew")
            status_entry = ttk.Combobox(review_table_frame, values=["Pass", "Fail"], width=8, state="readonly")
            status_entry.grid(row=review_row, column=2, sticky="nsew")
            comment_entry = tk.Entry(review_table_frame, width=30)
            comment_entry.grid(row=review_row, column=3, sticky="nsew")
            review_entries.append((str(script), status_entry, comment_entry))
            review_row += 1

    def on_next():
        # Collect review details and statuses
        review_details = review_details_text.get("1.0", tk.END).strip()
        overall_status = status_var.get()
        review_results = []
        for obj_name, status_entry, comment_entry in review_entries:
            status = status_entry.get()
            comment = comment_entry.get()
            review_results.append({"object": obj_name, "status": status, "comment": comment})
        # Optionally, store in shared_data or global for deployment tab
        if shared_data is not None:
            shared_data["review_details"] = review_details
            shared_data["overall_status"] = overall_status
            shared_data["review_results"] = review_results
        # Move to next tab (deployment)
        if notebook:
            idx = notebook.index(frame)
            if idx + 1 < notebook.index("end"):
                notebook.tab(idx + 1, state="normal")
                notebook.select(idx + 1)

    next_btn = tk.Button(frame, text="Next", command=on_next)
    next_btn.pack(side=tk.BOTTOM, pady=10)

    return frame
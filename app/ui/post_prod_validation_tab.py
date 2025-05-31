import tkinter as tk
from tkinter import ttk

def create_post_prod_validation_tab(notebook, home_frame=None):
    frame = ttk.Frame(notebook)

    # --- Preview Section ---
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

    # --- FixVersion Section ---
    fixversion_frame = ttk.Frame(frame)
    fixversion_frame.pack(fill=tk.X, padx=10, pady=(10, 2))
    fixversion_frame.columnconfigure(0, weight=1)
    fixversion_frame.columnconfigure(1, weight=0)
    fixversion_frame.columnconfigure(2, weight=0)
    fixversion_frame.columnconfigure(3, weight=1)
    ttk.Label(fixversion_frame, text="FixVersion:").grid(row=0, column=1, padx=(0, 8), pady=2)
    fixversion_var = tk.StringVar()
    fixversion_entry = ttk.Entry(fixversion_frame, textvariable=fixversion_var, width=30)
    fixversion_entry.grid(row=0, column=2, pady=2)

    # --- Fetch and Validate Buttons ---
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill=tk.X, padx=10, pady=(2, 10))
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=0)
    button_frame.columnconfigure(2, weight=0)
    button_frame.columnconfigure(3, weight=1)
    fetch_btn = ttk.Button(button_frame, text="Fetch")
    fetch_btn.grid(row=0, column=1, padx=(0, 10), pady=2)
    validate_btn = ttk.Button(button_frame, text="Validate")
    validate_btn.grid(row=0, column=2, pady=2)

    # --- Card Details Section ---
    card_details_frame = ttk.LabelFrame(frame, text="Card Details")
    card_details_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    # Container Frame for Canvas + Scrollbars
    card_table_container = ttk.Frame(card_details_frame)
    card_table_container.pack(fill=tk.BOTH, expand=True)

    # Canvas and Scrollbars
    canvas_card = tk.Canvas(
        card_table_container, highlightthickness=0, bg="#f5f5f5", bd=0, height=60
    )
    v_scrollbar_card = ttk.Scrollbar(card_table_container, orient="vertical", command=canvas_card.yview)
    h_scrollbar_card = ttk.Scrollbar(card_table_container, orient="horizontal", command=canvas_card.xview)

    v_scrollbar_card.pack(side="right", fill="y")
    h_scrollbar_card.pack(side="bottom", fill="x")
    canvas_card.pack(side="left", fill="both", expand=True, pady=2, padx=5, ipady=0, ipadx=0)

    canvas_card.configure(yscrollcommand=v_scrollbar_card.set, xscrollcommand=h_scrollbar_card.set)

    # Frame inside Canvas for table
    card_table_frame = ttk.Frame(canvas_card)
    canvas_card.create_window((0, 0), window=card_table_frame, anchor="nw")

    # --- Table Headers ---
    card_headers = ["JIRA#", "FixVersion", "Report Name", "SSIS", "Autosys", "SQLObjects", "Status"]
    for col, header_text in enumerate(card_headers):
        ttk.Label(
            card_table_frame, text=header_text, font=("TkDefaultFont", 10, "bold"),
            borderwidth=0, relief="solid", width=15
        ).grid(row=0, column=col, sticky="nsew", padx=4, pady=4)

    # --- Example Rows (replace with real data) ---
    example_rows = [
        ["JIRA-001", "1.0.0", "ReportA", "Yes", "No", "ObjX, ObjY", "Validated"],
        ["JIRA-002", "1.0.1", "ReportB", "No", "Yes", "ObjZ", "In Progress"],
        ["JIRA-003", "1.1.0", "ReportC", "Yes", "No", "ObjA, ObjB, ObjC", "Done"],
    ]

    for r, row_data in enumerate(example_rows, start=1):
        for c, value in enumerate(row_data):
            ttk.Label(
                card_table_frame, text=value, borderwidth=0, relief="solid", width=15
            ).grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

    # Configure Scroll Region on Frame Resize
    def on_card_frame_configure(event):
        canvas_card.configure(scrollregion=canvas_card.bbox("all"))

    card_table_frame.bind("<Configure>", on_card_frame_configure)

    return frame

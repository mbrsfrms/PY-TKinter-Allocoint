import tkinter as tk
from tkinter import messagebox
import logic


class BudgetFrame(tk.Frame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, bg="#CCFF00")
        self.app = app_instance
        self.font_name = self.app.main_font

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self, bg="#CCFF00")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=30)

        self.left_side = tk.Frame(self.container, bg="#CCFF00")
        self.left_side.pack(side="left", anchor="n", padx=(0, 30))

        tk.Label(
            self.left_side,
            text="Funds",
            font=(self.font_name, 24, "bold"),
            bg="#CCFF00",
            fg="#222222"
        ).pack(anchor="w", pady=(0, 4))

        f_row = tk.Frame(self.left_side, bg="#CCFF00")
        f_row.pack(fill="x", pady=3)

        tk.Label(
            f_row,
            text="Total Budget (Php)",
            font=(self.font_name, 12, "bold italic"),
            bg="#CCFF00",
            width=18,
            anchor="e"
        ).pack(side="left")

        self.total_entry = tk.Entry(
            f_row,
            bg="#222222",
            fg="white",
            font=(self.font_name, 13),
            width=14,
            justify="center"
        )
        self.total_entry.pack(side="left", padx=8, ipady=4)

        self.create_btn(f_row, self.set_funds).pack(side="left", padx=5)

        tk.Label(
            self.left_side,
            text="Allocation",
            font=(self.font_name, 24, "bold"),
            bg="#CCFF00",
            fg="#222222"
        ).pack(anchor="w", pady=(10, 4))

        self.name_entry = self.create_input_row(self.left_side, "Add Category")
        self.amt_entry = self.create_input_row(self.left_side, "Amount", has_btn=True)

        self.right_side = tk.Frame(self.container, bg="#CCFF00")
        self.right_side.pack(side="right", fill="both", expand=True)

        self.header = tk.Frame(self.right_side, bg="#CCFF00")
        self.header.pack(fill="x")

        self.header.grid_columnconfigure(0, weight=1, uniform="col")
        self.header.grid_columnconfigure(1, weight=1, uniform="col")

        tk.Label(
            self.header,
            text="Category",
            bg="#6200EE",
            fg="white",
            font=(self.font_name, 10, "bold"),
            pady=8
        ).grid(row=0, column=0, sticky="nsew", padx=2)

        tk.Label(
            self.header,
            text="Allocated",
            bg="#6200EE",
            fg="white",
            font=(self.font_name, 10, "bold"),
            pady=8
        ).grid(row=0, column=1, sticky="nsew", padx=2)

        self.table_container = tk.Frame(self.right_side, bg="#CCFF00")
        self.table_container.pack(fill="both", expand=True, pady=(3, 5))

        self.canvas = tk.Canvas(
            self.table_container,
            bg="#CCFF00",
            highlightthickness=0
        )

        self.scroll_frame = tk.Frame(self.canvas, bg="#CCFF00")

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw"
        )

        def _resize(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind("<Configure>", _resize)
        self.canvas.pack(fill="both", expand=True)

        def _scroll(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _scroll)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.rem_bar = tk.Label(
            self,
            text="Remaining funds: ₱0.00",
            bg="#FF2E97",
            fg="white",
            font=(self.font_name, 14, "bold"),
            pady=10
        )
        self.rem_bar.place(
            relx=0.5,
            rely=0.96,
            anchor="s",
            relwidth=0.82
        )

    def create_input_row(self, parent, label, has_btn=False):
        row = tk.Frame(parent, bg="#CCFF00")
        row.pack(fill="x", pady=3)

        tk.Label(
            row,
            text=label,
            font=(self.font_name, 12, "bold italic"),
            bg="#CCFF00",
            width=18,
            anchor="e"
        ).pack(side="left")

        entry = tk.Entry(
            row,
            bg="#222222",
            fg="white",
            font=(self.font_name, 13),
            width=14,
            justify="center"
        )
        entry.pack(side="left", padx=8, ipady=4)

        if has_btn:
            self.create_btn(row, self.add_cat).pack(side="left", padx=5)
        else:
            tk.Frame(row, bg="#CCFF00", width=80).pack(side="left")

        return entry

    def create_btn(self, parent, command):
        return tk.Button(
            parent,
            text="Confirm",
            bg="#FF2E97",
            fg="white",
            font=(self.font_name, 9, "bold"),
            borderwidth=0,
            padx=12,
            command=command,
            cursor="hand2"
        )

    def set_funds(self):
        try:
            self.app.total_funds = float(self.total_entry.get())
            self.app.update_all_uis()
        except:
            messagebox.showerror("Error", "Check total budget input")

    def add_cat(self):
        name = self.name_entry.get().strip()
        try:
            amt = float(self.amt_entry.get())

            if logic.validate_allocation(amt, self.app.total_funds, self.app.categories):
                self.app.categories[name] = logic.Category(name, amt)
                self.app.update_all_uis()
                self.name_entry.delete(0, tk.END)
                self.amt_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Limit", "Insufficient Funds")

        except:
            messagebox.showerror("Error", "Check amount input")

    def refresh_view(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for name, cat in self.app.categories.items():
            row = tk.Frame(self.scroll_frame, bg="#CCFF00")
            row.pack(fill="x", pady=1)

            # FIX: Added `uniform="col"` here as well so the rows exactly mirror the header logic
            row.grid_columnconfigure(0, weight=1, uniform="col")
            row.grid_columnconfigure(1, weight=1, uniform="col")

            tk.Label(
                row,
                text=name,
                bg="#6200EE",
                fg="white",
                font=(self.font_name, 9, "italic"),
                pady=8
            ).grid(row=0, column=0, sticky="nsew", padx=2)

            tk.Label(
                row,
                text=f"{cat.budget:,.0f}",
                bg="#6200EE",
                fg="white",
                font=(self.font_name, 9, "italic"),
                pady=8
            ).grid(row=0, column=1, sticky="nsew", padx=2)

        rem = logic.calculate_remaining_pool(
            self.app.total_funds,
            self.app.categories
        )

        self.rem_bar.config(
            text=f"Remaining funds: ₱{rem:,.2f}"
        )
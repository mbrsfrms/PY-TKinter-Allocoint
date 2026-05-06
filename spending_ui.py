import tkinter as tk
from tkinter import messagebox

class SpendingFrame(tk.Frame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, bg="#CCFF00")
        self.app = app_instance
        self.font_name = self.app.main_font

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_container = tk.Frame(self, bg="#CCFF00")
        self.main_container.grid(row=1, column=0)

        self.header_frame = tk.Frame(self.main_container, bg="#CCFF00")
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.header_frame.grid_columnconfigure(0, weight=1, uniform="col")
        self.header_frame.grid_columnconfigure(1, weight=1, uniform="col")
        self.header_frame.grid_columnconfigure(2, weight=1, uniform="col")

        tk.Label(
            self.header_frame,
            text="Category",
            bg="#6200EE",
            fg="white",
            font=(self.font_name, 11, "bold"),
            pady=18
        ).grid(row=0, column=0, sticky="nsew", padx=5)

        tk.Label(
            self.header_frame,
            text="Allocated (Remaining)",
            bg="#6200EE",
            fg="white",
            font=(self.font_name, 11, "bold"),
            pady=18
        ).grid(row=0, column=1, sticky="nsew", padx=5)

        tk.Label(
            self.header_frame,
            text="Expenses",
            bg="#FF2E97",
            fg="white",
            font=(self.font_name, 11, "bold"),
            pady=18
        ).grid(row=0, column=2, sticky="nsew", padx=5)

        self.clipper = tk.Frame(self.main_container, bg="#CCFF00", width=820, height=350)
        self.clipper.pack(pady=5)
        self.clipper.pack_propagate(False)

        self.canvas = tk.Canvas(self.clipper, bg="#CCFF00", highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="#CCFF00")

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.pack(fill="both", expand=True)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        self.funds_bar = tk.Label(
            self,
            text="Funds left: ₱0.00",
            bg="#FF2E97",
            fg="white",
            font=(self.font_name, 14, "bold italic"),
            pady=15
        )
        self.funds_bar.place(relx=0.5, rely=0.92, anchor="center", relwidth=0.5)

    def refresh_view(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        total_rem = 0.0

        for name, cat in self.app.categories.items():
            row = tk.Frame(self.scroll_frame, bg="#CCFF00")
            row.pack(fill="x", pady=2)

            row.grid_columnconfigure(0, weight=1, uniform="col")
            row.grid_columnconfigure(1, weight=1, uniform="col")
            row.grid_columnconfigure(2, weight=1, uniform="col")

            tk.Label(
                row,
                text=name,
                bg="#6200EE",
                fg="white",
                font=(self.font_name, 10, "italic"),
                pady=15
            ).grid(row=0, column=0, sticky="nsew", padx=5)

            tk.Label(
                row,
                text=f"{cat.balance:,.0f}",
                bg="#6200EE",
                fg="white",
                font=(self.font_name, 10, "italic"),
                pady=15
            ).grid(row=0, column=1, sticky="nsew", padx=5)

            entry = tk.Entry(
                row,
                bg="#FF2E97",
                fg="white",
                borderwidth=0,
                font=(self.font_name, 10, "bold"),
                justify="center",
                insertbackground="white"
            )
            
            entry.grid(row=0, column=2, sticky="nsew", padx=5, pady=2, ipady=8)

            entry.insert(0, "0")

            entry.bind("<FocusIn>", lambda e, ent=entry: ent.delete(0, tk.END))
            entry.bind("<Return>", lambda e, c=name, ent=entry: self.process_spend(c, ent))

            total_rem += cat.balance

        self.funds_bar.config(text=f"Funds left: ₱{total_rem:,.2f}")

    def process_spend(self, cat_name, entry_widget):
        try:
            amt = float(entry_widget.get())
            success, msg = self.app.categories[cat_name].record_expense(amt)

            if success:
                self.app.update_all_uis()
            else:
                messagebox.showwarning("Limit", msg)

        except ValueError:
            messagebox.showerror("Error", "Enter numeric value")
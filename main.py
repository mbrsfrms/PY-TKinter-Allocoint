import tkinter as tk
from tkinter import ttk
import budget_ui
import spending_ui

class AllocointApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Allocoint")
        self.root.geometry("1100x750")
        self.root.configure(bg="black")

        self.total_funds = 0.0
        self.categories = {}

        self.main_font = "Century Gothic"

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="black", borderwidth=0)
        style.configure("TNotebook.Tab", background="black", foreground="#CCFF00", 
                        font=(self.main_font, 14, "bold"), padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", "#CCFF00")], 
                  foreground=[("selected", "black")])

        tk.Label(root, text="Allocoint", font=(self.main_font, 52, "bold"), 
                 fg="#FF2E97", bg="black").pack(anchor="nw", padx=50, pady=30)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=50, pady=(0, 50))

        self.budget_tab = budget_ui.BudgetFrame(self.notebook, self)
        self.spending_tab = spending_ui.SpendingFrame(self.notebook, self)

        self.notebook.add(self.budget_tab, text="Manage Budget")
        self.notebook.add(self.spending_tab, text="Track Expenses")

    def update_all_uis(self):
        self.budget_tab.refresh_view()
        self.spending_tab.refresh_view()

if __name__ == "__main__":
    root = tk.Tk()
    app = AllocointApp(root)
    root.mainloop()
import tkinter as tk

from src.views.pages.ld.LDManager import LDManager_Page


class MainFrame(tk.Frame):
    def __init__(self, page):
        tk.Frame.__init__(self, bg='lightblue')
        self.canvas_scrollbar_pairs = []
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.Frame = page(self)
        self.canvas.create_window((0, 0), window=self.Frame, anchor="nw")
        if page == LDManager_Page:
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.Frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

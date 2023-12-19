import tkinter as tk

from views.layouts.MainFrame import MainFrame
from views.pages.FBManager import FBManager
from views.pages.LDManager import LDManager_Page
from views.pages.Setting import Setting
from constants.constants import LOGO_PATH
from utils.add_image import show_image


def close_app(app):
    app.destroy()


class SideBar(tk.Frame):
    def __init__(self, master, bg='lightblue'):
        super().__init__(master, bg=bg)
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.pack_propagate(False)
        self.configure(width=150)
        self.fb_service = None
        self.main_frame = MainFrame(LDManager_Page)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.border = tk.Label(self, borderwidth=1, relief='solid', padx=0)
        self.border.pack(side=tk.RIGHT, fill=tk.Y)

        img = show_image(self, LOGO_PATH, 80, 80)
        img.pack(padx=35, pady=50)

        self.button_LDManager = tk.Button(self, text="LDManager", width=150, height=2,
                                          command=lambda: self.choose_page(LDManager_Page))
        self.button_LDManager.pack(padx=5, pady=5)

        self.button_LDManager = tk.Button(self, text="Facebook Service", width=150, height=2,
                                          command=lambda: self.choose_popup(FBManager))
        self.button_LDManager.pack(padx=5, pady=5)

        self.button_setting = tk.Button(self, text="Setting", width=150, height=2,
                                        command=lambda: self.choose_page(Setting))
        self.button_setting.pack(padx=5, pady=5)

        self.button_exit = tk.Button(self, text="Exit", width=150, height=2,
                                     command=lambda: close_app(master))
        self.button_exit.pack(padx=5, pady=20, side=tk.BOTTOM)

    def choose_page(self, page):
        self.main_frame.destroy()
        self.main_frame = MainFrame(page)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def choose_popup(self, popup):
        if popup == FBManager:
            if self.fb_service is None:
                self.fb_service = FBManager(self)
            else:
                return

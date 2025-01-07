import tkinter as tk

from src.views.layouts.MainFrame import MainFrame
from src.views.pages.email.EmailManager import EmailManager
from src.views.pages.fb.FBManager import FBManager
from src.views.pages.home.HomePage import Home_Page
from src.views.pages.ld.LDManager import LDManager_Page
from src.views.pages.Setting import Setting
from src.constants.constants import LOGO_PATH
from src.utils.imageUtils import show_image


class SideBar(tk.Frame):
    def __init__(self, master, websocket, bg='lightblue'):
        super().__init__(master, bg=bg)
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.pack_propagate(False)
        self.configure(width=150)
        self.fb_service = None
        self.websocket = websocket
        self.main_frame = MainFrame(Home_Page)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.border = tk.Label(self, borderwidth=1, relief='solid', padx=0)
        self.border.pack(side=tk.RIGHT, fill=tk.Y)

        img = show_image(self, LOGO_PATH, 80, 80)
        img.pack(padx=35, pady=50)

        self.button_LDManager = tk.Button(self, text="Home", width=150, height=2,
                                          command=lambda: self.choose_page(Home_Page))
        self.button_LDManager.pack(padx=5, pady=5)

        self.button_LDManager = tk.Button(self, text="LDManager", width=150, height=2,
                                          command=lambda: self.choose_page(LDManager_Page))
        self.button_LDManager.pack(padx=5, pady=5)

        self.button_LDManager = tk.Button(self, text="Facebook Service", width=150, height=2,
                                          command=lambda: self.choose_popup(FBManager))
        self.button_LDManager.pack(padx=5, pady=5)

        self.button_EmailManager = tk.Button(self, text="Email Service", width=150, height=2,
                                             command=lambda: self.choose_page(EmailManager))
        self.button_EmailManager.pack(padx=5, pady=5)

        self.button_setting = tk.Button(self, text="Setting", width=150, height=2,
                                        command=lambda: self.choose_page(Setting))
        self.button_setting.pack(padx=5, pady=5)

        self.button_exit = tk.Button(self, text="Exit", width=150, height=2,
                                     command=lambda: master.on_close())
        self.button_exit.pack(padx=5, pady=20, side=tk.BOTTOM)

    def choose_page(self, page):
        self.main_frame.destroy()
        self.main_frame = MainFrame(page)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def choose_popup(self, popup):
        if popup == FBManager:
            if self.fb_service is None or self.fb_service.is_open is False:
                self.fb_service = FBManager(self)
            else:
                return

import tkinter as tk
from tkinter import ttk
import random

from src.enum.FBTaskEnum import FBTaskEnum
from src.ld_manager.get_list_ld import get_list_ld
from src.models.Facebook import FBAccount
from src.models.ListDevices import ListDevices
from src.models.tasks.FBTask import FacebookTask
from src.services.fbService import get_all_fb_accounts, get_ready_fb_accounts


class Home_Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        get_list_ld()
        self.ready_accounts = get_ready_fb_accounts(1)
        tk.Label(self, text=f"Tổng tài khoản FB : {len(self.ready_accounts)}").grid(row=0, column=3, sticky="w",
                                                                                    padx=20, pady=20)
        self.menu_bar = tk.Frame(self)
        self.menu_bar.grid(row=0, column=0, sticky="w", padx=20, pady=20)
        self.button_add = tk.Button(self.menu_bar, text="LIKE", width=10, height=2
                                    , command=lambda: self.choose_frame("LIKE"))
        self.button_add.grid(row=0, column=0, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="COMMENT", width=10, height=2
                                    , command=lambda: self.choose_frame("COMMENT"))
        self.button_get.grid(row=0, column=1, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="WATCH LIVE", width=10, height=2
                                    , command=lambda: self.choose_frame("WATCH LIVE"))
        self.button_get.grid(row=0, column=2, padx=5, pady=5)
        self.input_link_var = tk.StringVar()
        self.form_frame = tk.Frame(self)
        self.choose_frame("LIKE")

    def choose_frame(self, frame_name):
        self.form_frame.destroy()
        self.form_frame = tk.Frame(self)
        self.form_frame.grid(row=1, column=0, sticky="w", padx=20, pady=20)

        if frame_name == "LIKE":
            tk.Label(self.form_frame,
                     text="Like Bài Viết",
                     font=("Arial", 15)).grid(row=0, column=0, sticky="w", pady=5)

            tk.Label(self.form_frame,
                     text="Nhập ID bài viết",
                     font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=10)

            input_link_entry = ttk.Entry(self.form_frame,
                                         textvariable=self.input_link_var,
                                         width=50,
                                         font=("Arial", 11))
            input_link_entry.grid(row=1, column=1, sticky="w", pady=10)

            tk.Button(self.form_frame,
                      text="CHẠY",
                      width=10,
                      height=2,
                      command=lambda: self.run_task(FBTaskEnum.LIKE_POST)).grid(row=2, column=1, sticky="w",
                                                                                      pady=5)

        if frame_name == "COMMENT":
            tk.Label(self.form_frame,
                     text="Tăng comment",
                     font=("Arial", 15)).grid(row=0, column=0, sticky="w", pady=5)

        if frame_name == "WATCH LIVE":
            tk.Label(self.form_frame,
                     text="Tăng mắt Livestream",
                     font=("Arial", 15)).grid(row=0, column=0, sticky="w", pady=5)

    def run_task(self, selected_option):
        list_account = self.ready_accounts
        while len(list_account) > 0:
            if len(list_account) > 14:
                random_accounts = random.sample(list_account, 15)
            else:
                random_accounts = list_account

            for account in random_accounts:
                list_account.remove(account)

            if selected_option == FBTaskEnum.LIKE_POST:
                task = FacebookTask(function="",
                                    args=None,
                                    list_account=random_accounts,
                                    name=FBTaskEnum.LIKE_POST.value)
                if self.input_link_var.get() == "":
                    return
                task.args = (self.input_link_var.get(),)
                task.function = task.like_post
                ListDevices.add_task(task)



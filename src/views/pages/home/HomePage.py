import random
import threading
import time
import tkinter as tk
from tkinter import ttk

from src.constants.constants import LAMNGOCTHANH_PAGEID, LAMNGOCTHANH_ACCESSTOKEN, HCSPA_PAGEID, \
    HCSPA_PAGEID_ACCESSTOKEN
from src.enum.FBTaskEnum import FBTaskEnum
from src.ld_manager.get_list_ld import get_list_ld
from src.models.ListDevices import ListDevices
from src.models.tasks.FBTask import FacebookTask
from src.services.fbService import get_ready_fb_accounts
from src.services.pageService import get_posts, check_new_posts

count = 0


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
        self.button_get = tk.Button(self.menu_bar, text="AUTO", width=10, height=2
                                    , command=lambda: self.choose_frame("AUTO"))
        self.button_get.grid(row=0, column=1, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="WATCH LIVE", width=10, height=2
                                    , command=lambda: self.choose_frame("WATCH LIVE"))
        self.button_get.grid(row=0, column=2, padx=5, pady=5)
        self.input_link_var = tk.StringVar()
        self.form_frame = tk.Frame(self)
        self.choose_frame("LIKE")
        self.auto_mode = False
        Home_Page.result = tk.Label(self)

    def choose_frame(self, frame_name):
        if ListDevices.is_running:
            return
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

            tk.Label(self.form_frame, text="Like đã tăng", font=("Arial", 11)).grid(row=2, column=0, sticky="w",
                                                                                    pady=10)
            Home_Page.result = tk.Label(self.form_frame, text="0", font=("Arial", 11))
            Home_Page.result.grid(row=2, column=1, sticky="w", pady=10)

            tk.Button(self.form_frame,
                      text="CHẠY",
                      width=10,
                      height=2,
                      command=lambda: self.run_task(FBTaskEnum.LIKE_POST)).grid(row=3, column=1, sticky="w",
                                                                                pady=5)

        if frame_name == "AUTO":
            tk.Button(self.form_frame,
                      text="BẮT ĐẦU",
                      width=10,
                      height=2,
                      font=("Arial", 15),
                      command=self.auto_clicked).grid(row=0, column=0, sticky="w", pady=5)
            tk.Button(self.form_frame,
                      text="DỪNG",
                      width=10,
                      height=2,
                      font=("Arial", 15),
                      command=self.off_auto).grid(row=0, column=1, sticky="w", pady=5)

        if frame_name == "WATCH LIVE":
            tk.Label(self.form_frame,
                     text="Tăng mắt Livestream",
                     font=("Arial", 15)).grid(row=0, column=0, sticky="w", pady=5)

    def run_task(self, selected_option):
        list_account = self.ready_accounts
        Home_Page.count = 0
        while list_account:
            selected_elements = random.sample(list_account, min(10, len(list_account)))

            if selected_option == FBTaskEnum.LIKE_POST:
                task = FacebookTask(function="",
                                    args=None,
                                    list_account=selected_elements,
                                    name=FBTaskEnum.LIKE_POST.value)
                if self.input_link_var.get() == "":
                    return
                task.args = (self.input_link_var.get(),)
                task.function = task.like_post
                ListDevices.add_task(task)

            list_account = [element for element in list_account if element not in selected_elements]

    def auto_clicked(self):
        if not self.auto_mode:
            self.auto_mode = True
            thread = threading.Thread(target=self.auto_like_task)
            thread.start()

    def auto_like_task(self):
        while self.auto_mode:
            if not self.auto_mode:
                return
            if ListDevices.is_running:
                time.sleep(60)
                continue
            post_ids = get_posts(LAMNGOCTHANH_PAGEID, LAMNGOCTHANH_ACCESSTOKEN)
            post_ids = post_ids + get_posts(HCSPA_PAGEID, HCSPA_PAGEID_ACCESSTOKEN)
            print(post_ids)
            post_id = check_new_posts(post_ids)
            # post_id = ['238210359712854_786052973541779']
            if post_id:
                print(f"found new posts {post_id}")
                list_account = self.ready_accounts
                while list_account:
                    selected_elements = random.sample(list_account, min(10, len(list_account)))
                    task = FacebookTask(function="",
                                        args=None,
                                        list_account=selected_elements,
                                        name=FBTaskEnum.LIKE_POST.value,
                                        cooldown=len(post_id))
                    task.args = (post_id,)
                    task.function = task.like_post
                    ListDevices.add_task(task)

                    list_account = [element for element in list_account if element not in selected_elements]

            else:
                print("NO NEW POSTS")
                time.sleep(150)
                continue

    def off_auto(self):
        self.auto_mode = False

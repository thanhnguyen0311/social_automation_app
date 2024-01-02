import threading
import time
import tkinter as tk
from tkinter import ttk

from src.enum.EmailEnum import EmailActionEnum
from src.ld_manager.run_ld import run_list_ld
from src.remote.email.register import register_email
from src.views.pages.email.AddPopup import AddEmail
from src.views.pages.email.EmailTree import MailList


class EmailManager(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs, bg='white')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.add_email_popup = None
        self.style.configure('Treeview', rowheight=25)
        button_frame = tk.Frame(self, bg='white')
        button_frame.pack(padx=5, pady=20, anchor=tk.NW, fill=tk.BOTH)
        button_add = tk.Button(button_frame,
                               text="ADD",
                               width=10, height=1,
                               command=lambda: self.choose_popup(AddEmail))
        button_add.grid(row=0, column=0, padx=5)
        button_refresh = tk.Button(button_frame,
                                   text="REFRESH",
                                   width=10, height=1, command=lambda: self.mail_list.on_refresh_clicked())
        button_refresh.grid(row=0, column=1, padx=5)
        button_remove = tk.Button(button_frame,
                                  text="REMOVE",
                                  width=10, height=1)
        button_remove.grid(row=0, column=2, padx=5)

        self.option = tk.StringVar()
        self.option.set(EmailActionEnum.NO_ACTION.value)
        option_menu = ttk.Combobox(button_frame,
                                   textvariable=self.option,
                                   values=[option.value for option in EmailActionEnum])
        option_menu.grid(row=1, column=0, columnspan=2,
                         padx=5, pady=10, sticky=tk.NSEW)

        button_action = tk.Button(button_frame,
                                  text="RUN",
                                  width=10, height=1,
                                  command=self.on_option_selected)
        button_action.grid(row=1, column=2,
                           padx=5, pady=10, sticky=tk.W)

        self.mail_list = MailList(self)
        self.mail_list.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def choose_popup(self, popup):
        if popup == AddEmail:
            if self.add_email_popup is None or self.add_email_popup.is_open is False:
                self.add_email_popup = AddEmail(self)
            else:
                return

    def on_option_selected(self):
        selected_option = self.option.get()
        list_account = self.mail_list.get_selected()

        list_account = run_list_ld(list_account)

        if selected_option == EmailActionEnum.CREATE.value:
            for account in list_account:
                account.thread = threading.Thread(target=register_email, args=(account,))
                account.thread.start()
                time.sleep(3)

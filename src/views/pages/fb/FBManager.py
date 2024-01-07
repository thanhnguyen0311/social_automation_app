import tkinter as tk
from tkinter import ttk

from src.enum.FBTaskEnum import FBTaskEnum
from src.models.ListDevices import ListDevices
from src.models.tasks.FBTask import FacebookTask
from src.views.pages.fb.AccountsTree import FBAccountsList
from src.views.pages.fb.AddPopup import AddFacebookAccount


class FBManager(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, bg='lightblue')
        self.title("Facebook Service")
        self.geometry("1200x600")
        self.show_checkpoint = tk.BooleanVar()
        self.show_insecure = tk.BooleanVar()
        self.is_open = True
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.fb_account_list = FBAccountsList(self, self.show_checkpoint, self.show_insecure)
        self.add_fb_popup = None
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', rowheight=25)

        button_frame = tk.Frame(self, bg='lightblue')
        button_frame.pack(padx=5, pady=20, anchor=tk.NW)

        button_add = tk.Button(button_frame,
                               text="ADD",
                               width=10, height=1,
                               command=lambda: self.choose_popup(AddFacebookAccount))
        button_add.grid(row=0, column=0, padx=5)

        button_refresh = tk.Button(button_frame,
                                   text="REFRESH",
                                   width=10, height=1,
                                   command=lambda: self.fb_account_list.on_refresh_clicked())
        button_refresh.grid(row=0, column=1, padx=5)

        button_remove = tk.Button(button_frame,
                                  text="REMOVE",
                                  width=10, height=1,
                                  command=lambda: self.fb_account_list.remove_accounts())
        button_remove.grid(row=0, column=2, padx=5)

        button_remove = tk.Button(button_frame,
                                  text="CLOSE",
                                  width=10, height=1,
                                  command=self.close_task)
        button_remove.grid(row=0, column=3, padx=5)

        self.option = tk.StringVar()
        self.option.set(FBTaskEnum.NO_ACTION.value)
        option_menu = ttk.Combobox(button_frame,
                                   textvariable=self.option,
                                   width=20,
                                   height=20,
                                   font="Verdana 8 bold",
                                   values=[option.value for option in FBTaskEnum])
        option_menu.grid(row=1, column=0, columnspan=3,
                         padx=5, pady=10, sticky=tk.NSEW)

        button_action = tk.Button(button_frame,
                                  text="RUN",
                                  width=10, height=1,
                                  command=self.on_option_selected)
        button_action.grid(row=1, column=3,
                           padx=5, pady=10, sticky=tk.W)

        self.fb_account_list.pack(padx=10, pady=5,
                                  fill=tk.BOTH, expand=True)

        self.filter_frame = tk.Frame(self, bg='lightblue')
        self.display_filter_frame()

    def on_close(self):
        self.destroy()
        self.is_open = False

    def close_task(self):
        ListDevices.cancel_current_task()
        pass

    def on_option_selected(self):
        selected_option = self.option.get()
        list_account = self.fb_account_list.get_selected()

        task = FacebookTask(function="",
                            args=None,
                            list_account=list_account,
                            name="")
        task_mapping = {
            FBTaskEnum.LOGIN: task.login,
            FBTaskEnum.REGISTER: task.register,
            FBTaskEnum.NEW_FEED: task.farm_new_feed,
        }
        selected_enum = FBTaskEnum(selected_option)

        if selected_enum in task_mapping:
            task.name = selected_enum.value
            task.function = task_mapping[selected_enum]

        ListDevices.add_task(task)

    def choose_popup(self, popup):
        if popup == AddFacebookAccount:
            if self.add_fb_popup is None or self.add_fb_popup.is_open is False:
                self.add_fb_popup = AddFacebookAccount(self)
            else:
                return

    def display_filter_frame(self):
        tk.Checkbutton(self.filter_frame, text="Show check-point",
                       variable=self.show_checkpoint,
                       bg='lightblue',
                       font=("Arial", 9, 'bold'),
                       command=self.fb_account_list.on_refresh_clicked).pack(pady=2, padx=10, anchor=tk.W)

        tk.Checkbutton(self.filter_frame, text="Show only insecure ",
                       variable=self.show_insecure,
                       bg='lightblue',
                       font=("Arial", 9, 'bold'),
                       command=self.fb_account_list.on_refresh_clicked).pack(pady=2, padx=10, anchor=tk.W)

        self.filter_frame.place(relx=1, rely=0.1, anchor=tk.NE)

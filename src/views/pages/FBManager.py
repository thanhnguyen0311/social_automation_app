import tkinter as tk
from tkinter import ttk

from ttkbootstrap import Style

from src.controller.addFB import AddFacebookController
from src.enum.taskEnum import TaskEnum
from src.models.Email import EmailAccount
from src.models.Facebook import FBAccount
from src.remote.facebook.login import login_facebook
from src.services.fbService import get_all_fb_accounts, remove_fb_accounts
from src.utils.randomGenerate import generate_random_password


class FBManager(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs, bg='lightblue')
        self.title("Facebook Service")
        self.geometry("1200x600")
        self.is_open = True
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.fb_account_list = FBAccountsList(self)
        self.add_fb_popup = None
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', rowheight=25)
        button_frame = tk.Frame(self, bg='lightblue')
        button_frame.pack(padx=5, pady=20, anchor=tk.NW)
        button_add = tk.Button(button_frame, text="ADD", width=10, height=1,
                               command=lambda: self.choose_popup(AddFacebookAccount))
        button_add.grid(row=0, column=0, padx=5)
        button_refresh = tk.Button(button_frame, text="REFRESH", width=10, height=1,
                                   command=lambda: self.fb_account_list.refresh())
        button_refresh.grid(row=0, column=1, padx=5)
        button_remove = tk.Button(button_frame, text="REMOVE", width=10, height=1,
                                  command=lambda: self.fb_account_list.remove_accounts())
        button_remove.grid(row=0, column=2, padx=5)

        self.options = ["Choose an action", "Check Account"]
        self.option = tk.StringVar()
        self.option.set(TaskEnum.NO_ACTION.value)
        option_menu = ttk.Combobox(button_frame, textvariable=self.option, values=[option.value for option in TaskEnum])
        option_menu.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky=tk.W)

        button_action = tk.Button(button_frame, text="RUN", width=10, height=1, command=self.on_option_selected)
        button_action.grid(row=1, column=2, padx=5, pady=10, sticky=tk.W)
        self.fb_account_list.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def on_close(self):
        self.destroy()
        self.is_open = False

    def on_option_selected(self):
        selected_option = self.option.get()
        list_account = self.fb_account_list.get_selected()
        if selected_option == TaskEnum.LOGIN.value:
            for account in list_account:
                print(account.facebook_account_id)
                login_facebook(account)

    def choose_popup(self, popup):
        if popup == AddFacebookAccount:
            if self.add_fb_popup is None or self.add_fb_popup.is_open is False:
                self.add_fb_popup = AddFacebookAccount(self)
            else:
                return


class FBAccountsList(ttk.Treeview):
    def __init__(self, master):
        ttk.Treeview.__init__(self, master,
                              columns=("ID", "Name", "email", "password",
                                       "device", "status", "last_login",
                                       "create_date", "live"),
                              show="headings", selectmode="extended")
        self.heading("ID", text="ID")
        self.heading("Name", text="Name")
        self.heading("email", text="Email")
        self.heading("password", text="Password")
        self.heading("device", text="Device")
        self.heading("status", text="Status")
        self.heading("last_login", text="Last login")
        self.heading("create_date", text="Create date")
        self.heading("live", text="Live Record")

        self.column("ID", width=5, anchor='center')
        self.column("Name", width=50, anchor='center')
        self.column("email", width=120, anchor='center')
        self.column("password", width=80, anchor='center')
        self.column("device", width=50, anchor='center')
        self.column("status", width=50, anchor='center')
        self.column("last_login", width=50, anchor='center')
        self.column("create_date", width=50, anchor='center')
        self.column("live", width=80, anchor='center')

        self.data = []
        self.refresh()

    def get_selected(self):
        list_account = []
        for item in self.selection():
            for account in self.data:
                if int(item) == account.facebook_account_id:
                    list_account.append(account)

        return list_account

    def remove_accounts(self):
        for item in self.selection():
            if remove_fb_accounts(item) is True:
                print("Deleted account id {0}".format(item))
        self.refresh()

    def refresh(self):
        self.delete(*self.get_children())
        self.data = get_all_fb_accounts(1)
        for account in self.data:
            if account.is_deleted:
                continue

            item_id = self.insert("", "end", iid=account.facebook_account_id,
                                  values=(account.facebook_account_id,
                                          account.first_name + " " + account.last_name,
                                          account.email.email_address,
                                          account.password,
                                          account.device,
                                          account.status,
                                          account.last_login,
                                          account.create_date,
                                          ""))


class AddFacebookAccount(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs, padx=20, pady=20, bg='lightblue')
        self.title("Add Facebook Account")
        self.geometry("450x250")
        self.geometry("+500+100")
        self.is_open = True
        self.master.fb_account_list = master.fb_account_list
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.resizable(False, False)
        model = FBAccount(email=EmailAccount(first_name='Thanh',
                                             last_name='Nguyen',
                                             password='Danny@0311',
                                             email_address='nct031194@icloud.com'),
                          first_name='Thanh',
                          last_name='Nguyen',
                          password='Danny@0311')
        self.controller = AddFacebookController(model, self)
        self.set_controller(self.controller)

        tk.Label(self, text="Email: ", font=("Helvetica", 10), bg='lightblue').grid(row=0, column=0, sticky=tk.W,
                                                                                    pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=20, font=("Helvetica", 11))
        self.email_entry.grid(row=0, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Password: ", font=("Helvetica", 10), bg='lightblue').grid(row=1, column=0, sticky=tk.W,
                                                                                       pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, width=20, font=("Helvetica", 11))
        self.password_entry.grid(row=1, column=1, columnspan=4, sticky=tk.NSEW, pady=5)
        tk.Button(self,
                  text="Generate",
                  command=self.generate_password).grid(row=1, column=5, sticky=tk.W, pady=5, padx=5)

        tk.Label(self,
                 text="EPassword: ",
                 font=("Helvetica", 10), bg='lightblue').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_password_var = tk.StringVar()
        self.email_password_entry = ttk.Entry(self, textvariable=self.email_password_var, width=20,
                                              font=("Helvetica", 11))
        self.email_password_entry.grid(row=2, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self,
                 text="First Name: ",
                 font=("Helvetica", 10),
                 bg='lightblue').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(self, textvariable=self.first_name_var, width=9, font=("Helvetica", 11))
        self.first_name_entry.grid(row=3, column=1, sticky=tk.NSEW, pady=5)

        tk.Label(self,
                 text="Last Name: ",
                 font=("Helvetica", 10),
                 bg='lightblue').grid(row=3, column=3, sticky=tk.N, pady=5)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(self, textvariable=self.last_name_var, width=9, font=("Helvetica", 11))
        self.last_name_entry.grid(row=3, column=4, sticky=tk.NSEW, pady=5)

        tk.Button(self,
                  text="Submit",
                  font=("Helvetica", 10),
                  command=self.save_button_clicked).grid(row=4, column=1, sticky=tk.NSEW, pady=15)
        tk.Button(self,
                  text=" Cancel ",
                  font=("Helvetica", 10),
                  command=self.on_close).grid(row=4, column=3, sticky=tk.NSEW, pady=15, padx=20)

        self.generate_password()

        self.message_label = ttk.Label(self, text='', background='lightblue')
        self.message_label.grid(row=5, column=1, columnspan=5, sticky=tk.NW)

    def on_close(self):
        self.destroy()
        self.is_open = False
        self.master.fb_account_list.refresh()

    def generate_password(self):
        new_password = generate_random_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_password)
        self.email_password_entry.delete(0, tk.END)
        self.email_password_entry.insert(0, new_password)

    def save_button_clicked(self):
        if self.controller:
            self.controller.save({
                'email': self.email_var.get(),
                'password': self.password_var.get(),
                'email_password': self.email_password_var.get(),
                'first_name': self.first_name_var.get(),
                'last_name': self.last_name_var.get()
            })

    def set_controller(self, controller):
        self.controller = controller

    def show_success(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.reset_form()

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'

    def hide_message(self):
        self.message_label['text'] = ''

    def reset_form(self):
        self.generate_password()
        self.email_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)

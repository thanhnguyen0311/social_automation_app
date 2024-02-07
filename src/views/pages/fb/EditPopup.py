import tkinter as tk
from tkinter import ttk

from src.controller.editFB import EditFacebookController
from src.services.emailService import get_email_for_facebook
from src.services.fbService import find_fb_account_by_ID


class EditFacebookAccount(tk.Toplevel):
    def __init__(self, master, account_iid):
        tk.Toplevel.__init__(self, master, padx=20, pady=20, bg='lightblue')
        self.title("Edit Facebook Account")
        self.geometry("550x550")
        self.geometry("+500+100")
        self.is_open = True
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.resizable(False, False)
        self.account = find_fb_account_by_ID(account_iid)
        self.emails = get_email_for_facebook(1)
        self.controller = EditFacebookController(self.account, self)
        self.set_controller(self.controller)

        tk.Label(self, text="Email: ", font=("Helvetica", 10), bg='lightblue').grid(row=0, column=0, sticky=tk.W,
                                                                                    pady=5)
        self.email_var = tk.StringVar()
        if self.account.email:
            self.email_var.set(self.account.email.email_address)
            email = ttk.Entry(self, textvariable=self.email_var, width=25)
        else:
            self.email_var.set("Choose an email")
            email = ttk.Combobox(self,
                                 textvariable=self.email_var, width=25,
                                 values=[value.email_address for value in self.emails.values()])

        email.grid(row=0, column=1, columnspan=4,
                   padx=5, pady=10, sticky=tk.NSEW)

        tk.Label(self, text="Password: ", font=("Arial", 10), bg='lightblue').grid(row=1, column=0, sticky=tk.W,
                                                                                   pady=5)
        self.password_var = tk.StringVar()
        self.password_var.set(self.account.password)
        password = ttk.Entry(self, textvariable=self.password_var, width=25, font=("Arial", 11))
        password.grid(row=1, column=1, columnspan=4,
                      padx=5, pady=10, sticky=tk.NSEW)

        tk.Label(self,
                 text="First Name: ",
                 font=("Arial", 10),
                 bg='lightblue').grid(row=2, column=0, sticky=tk.W, pady=5)

        self.first_name_var = tk.StringVar()
        self.first_name_var.set(self.account.first_name)
        self.first_name_entry = ttk.Entry(self, textvariable=self.first_name_var, width=9, font=("Arial", 11))
        self.first_name_entry.grid(row=2, column=1, sticky=tk.NSEW, pady=5)

        tk.Label(self,
                 text="Last Name: ",
                 font=("Arial", 10),
                 bg='lightblue').grid(row=2, column=3, sticky=tk.N, pady=5)
        self.last_name_var = tk.StringVar()
        self.last_name_var.set(self.account.last_name)
        self.last_name_entry = ttk.Entry(self, textvariable=self.last_name_var, width=9, font=("Arial", 11))
        self.last_name_entry.grid(row=2, column=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Token: ", font=("Arial", 10), bg='lightblue').grid(row=3, column=0, sticky=tk.W,
                                                                                pady=5)
        self.token_var = tk.StringVar()
        self.token_var.set(self.account.token)
        self.token_entry = ttk.Entry(self, textvariable=self.token_var, width=20, font=("Arial", 11))
        self.token_entry.grid(row=3, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="2FA: ", font=("Arial", 10), bg='lightblue').grid(row=4, column=0, sticky=tk.W,
                                                                              pady=5)
        self.auth2fa_var = tk.StringVar()
        self.auth2fa_entry = ttk.Entry(self, textvariable=self.auth2fa_var, width=20, font=("Arial", 11))
        self.auth2fa_entry.grid(row=4, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="UID: ", font=("Arial", 10), bg='lightblue').grid(row=5, column=0, sticky=tk.W,
                                                                              pady=5)
        self.uid_var = tk.StringVar()
        self.uid_var.set(self.account.uid)
        self.uid_entry = ttk.Entry(self, textvariable=self.uid_var, width=20, font=("Arial", 11))
        self.uid_entry.grid(row=5, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Cookie: ", font=("Arial", 10), bg='lightblue').grid(row=6, column=0, sticky=tk.W,
                                                                                 pady=5)
        self.cookie_var = tk.StringVar()
        self.cookie_var.set(self.account.cookie)
        self.cookie_entry = ttk.Entry(self, textvariable=self.cookie_var, width=20, font=("Arial", 11))
        self.cookie_entry.grid(row=6, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Clone Target UID: ", font=("Arial", 10), bg='lightblue').grid(row=7, column=0,
                                                                                           sticky=tk.W,
                                                                                           pady=5)
        self.clone_uid_var = tk.StringVar()
        self.clone_uid_var.set(self.account.clone_target_uid)
        self.clone_uid_entry = ttk.Entry(self, textvariable=self.clone_uid_var, width=20, font=("Arial", 11))
        self.clone_uid_entry.grid(row=7, column=1, columnspan=2, sticky=tk.W, pady=5)

        self.is_secure_var = tk.BooleanVar()
        self.is_secure_var.set(self.account.secure)
        tk.Checkbutton(self, text="Is secure?",
                       variable=self.is_secure_var,
                       bg='lightblue',
                       font=("Arial", 9, 'bold')).grid(row=8, column=1, columnspan=4, sticky=tk.W, pady=5)

        tk.Button(self,
                  text="Submit",
                  font=("Arial", 10),
                  command=self.save_button_clicked).grid(row=9, column=1, sticky=tk.NSEW, pady=15)
        tk.Button(self,
                  text=" Cancel ",
                  font=("Arial", 10),
                  command=self.on_close).grid(row=9, column=3, sticky=tk.NSEW, pady=15, padx=20)

        self.message_label = ttk.Label(self, text='', background='lightblue')
        self.message_label.grid(row=10, column=1, columnspan=5, sticky=tk.NW)

    def on_close(self):
        self.destroy()
        self.is_open = False

    def set_controller(self, controller):
        self.controller = controller

    def show_success(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.on_close()

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'

    def hide_message(self):
        self.message_label['text'] = ''

    def save_button_clicked(self):
        pass

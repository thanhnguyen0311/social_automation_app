import tkinter as tk
from tkinter import ttk

from src.controller.addFB import AddFacebookController
from src.models.Email import EmailAccount
from src.models.Facebook import FBAccount
from src.services.emailService import get_email_for_facebook
from src.utils.randomGenerate import generate_random_password


class AddFacebookAccount(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs, padx=20, pady=20, bg='lightblue')
        self.title("Add Facebook Account")
        self.geometry("550x550")
        self.geometry("+500+100")
        self.is_open = True
        self.master.fb_account_list = master.fb_account_list
        self.grab_set()
        self.emails = get_email_for_facebook(1)
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
        self.email_var.set("Choose an email")

        email_list = ttk.Combobox(self,
                                  textvariable=self.email_var, width=25,
                                  values=[value.email_address for value in self.emails.values()])
        email_list.grid(row=0, column=1, columnspan=4,
                        padx=5, pady=10, sticky=tk.NSEW)
        email_list.bind("<<ComboboxSelected>>", self.on_combobox_change)

        tk.Label(self, text="Password: ", font=("Arial", 10), bg='lightblue').grid(row=1, column=0, sticky=tk.W,
                                                                                   pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, width=20, font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, columnspan=4, sticky=tk.NSEW, pady=5)
        tk.Button(self,
                  text="Generate",
                  command=self.generate_password).grid(row=1, column=5, sticky=tk.W, pady=5, padx=5)

        tk.Label(self,
                 text="First Name: ",
                 font=("Arial", 10),
                 bg='lightblue').grid(row=2, column=0, sticky=tk.W, pady=5)

        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(self, textvariable=self.first_name_var, width=9, font=("Arial", 11))
        self.first_name_entry.grid(row=2, column=1, sticky=tk.NSEW, pady=5)

        tk.Label(self,
                 text="Last Name: ",
                 font=("Arial", 10),
                 bg='lightblue').grid(row=2, column=3, sticky=tk.N, pady=5)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(self, textvariable=self.last_name_var, width=9, font=("Arial", 11))
        self.last_name_entry.grid(row=2, column=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Token: ", font=("Arial", 10), bg='lightblue').grid(row=3, column=0, sticky=tk.W,
                                                                                pady=5)
        self.token_var = tk.StringVar()
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
        self.uid_entry = ttk.Entry(self, textvariable=self.uid_var, width=20, font=("Arial", 11))
        self.uid_entry.grid(row=5, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Cookie: ", font=("Arial", 10), bg='lightblue').grid(row=6, column=0, sticky=tk.W,
                                                                                 pady=5)
        self.cookie_var = tk.StringVar()
        self.cookie_entry = ttk.Entry(self, textvariable=self.cookie_var, width=20, font=("Arial", 11))
        self.cookie_entry.grid(row=6, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Clone Target UID: ", font=("Arial", 10), bg='lightblue').grid(row=7, column=0,
                                                                                           sticky=tk.W,
                                                                                           pady=5)
        self.clone_uid_var = tk.StringVar()
        self.clone_uid_entry = ttk.Entry(self, textvariable=self.clone_uid_var, width=20, font=("Arial", 11))
        self.clone_uid_entry.grid(row=7, column=1, columnspan=2, sticky=tk.W, pady=5)

        self.is_secure_var = tk.BooleanVar()
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

        self.generate_password()

        self.message_label = ttk.Label(self, text='', background='lightblue')
        self.message_label.grid(row=10, column=1, columnspan=5, sticky=tk.NW)

    def on_combobox_change(self, event):
        for email in self.emails.values():
            if email.email_address == self.email_var.get():
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, email.password)
                self.first_name_entry.delete(0, tk.END)
                self.first_name_entry.insert(0, email.first_name)
                self.last_name_entry.delete(0, tk.END)
                self.last_name_entry.insert(0, email.last_name)

    def on_close(self):
        self.destroy()
        self.is_open = False
        self.master.fb_account_list.on_refresh_clicked()

    def generate_password(self):
        new_password = generate_random_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_password)

    def save_button_clicked(self):
        if self.controller:
            email = self.email_var.get()
            if email == "Choose an email":
                email = None
            self.controller.save({
                'email': email,
                'password': self.password_var.get(),
                'first_name': self.first_name_var.get(),
                'last_name': self.last_name_var.get(),
                'auth_2fa': self.auth2fa_var.get(),
                'cookie': self.cookie_var.get(),
                'uid': self.uid_var.get(),
                'token': self.token_var.get(),
                'secure': self.is_secure_var.get(),
                'clone_target_uid': self.clone_uid_var.get()
            })

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

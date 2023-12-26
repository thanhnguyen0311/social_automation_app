import tkinter as tk
from tkinter import ttk

from src.controller.addFB import AddFacebookController
from src.models.Email import EmailAccount
from src.models.Facebook import FBAccount
from src.utils.randomGenerate import generate_random_password


class AddFacebookAccount(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs, padx=20, pady=20, bg='lightblue')
        self.title("Add Facebook Account")
        self.geometry("550x250")
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
        self.master.fb_account_list.on_refresh_clicked()

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

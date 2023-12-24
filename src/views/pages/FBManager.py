import tkinter as tk
from tkinter import ttk

from ttkbootstrap import Style


class FBManager(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs, bg='lightblue')
        self.title("Facebook Service")
        self.geometry("800x600")
        self.is_open = True
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.fb_account_list = FBAccountsList(self)
        self.add_fb_popup = None
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', rowheight=25)
        button_frame = tk.Frame(self, bg='lightblue')
        button_frame.pack(padx=5, pady=20, anchor=tk.NW)
        button_add = tk.Button(button_frame, text="ADD", width=10, height=2,
                               command=lambda: self.choose_popup(AddFacebookAccount))
        button_add.grid(row=0, column=0, padx=5)
        button_refresh = tk.Button(button_frame, text="REFRESH", width=10, height=2)
        button_refresh.grid(row=0, column=1, padx=5)
        button_remove = tk.Button(button_frame, text="REMOVE", width=10, height=2)
        button_remove.grid(row=0, column=2, padx=5)
        button_action = tk.Button(button_frame, text="RUN TASK", width=10, height=2)
        button_action.grid(row=0, column=3, padx=5)
        self.fb_account_list.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def on_close(self):
        self.destroy()
        self.is_open = False

    def choose_popup(self, popup):
        if popup == AddFacebookAccount:
            if self.add_fb_popup is None or self.add_fb_popup.is_open is False:
                self.add_fb_popup = AddFacebookAccount(self)
            else:
                return


class FBAccountsList(ttk.Treeview):
    def __init__(self, master):
        ttk.Treeview.__init__(self, master,
                              columns=("ID", "email", "password", "device", "status", "action"),
                              show="headings", selectmode="extended")
        self.heading("ID", text="ID")
        self.heading("email", text="Email")
        self.heading("password", text="Password")
        self.heading("device", text="Device")
        self.heading("status", text="Status")
        self.heading("action", text="Action")

        self.column("ID", width=10, anchor='center')
        self.column("email", width=120, anchor='center')
        self.column("password", width=80, anchor='center')
        self.column("device", width=120, anchor='center')
        self.column("status", width=50, anchor='center')
        self.column("action", width=50, anchor='center')

        data = [
            (0, 'nct031194@icloud.com', '272337839', 'IMEI: 123124512512', 'Offline')
        ]

        for i, (ID, email, password, device, status) in enumerate(data):
            item_id = self.insert("", "end", iid=ID,
                                  values=(ID, email, password, device, status))

    def show_selected(self):
        for item in self.selection():
            print(item)


class AddFacebookAccount(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs, padx=20, pady=20, bg='lightblue')
        self.title("Add Facebook Account")
        self.geometry("450x300")
        self.geometry("+500+100")
        self.is_open = True
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.resizable(False, False)

        tk.Label(self, text="Email: ", font=("Helvetica", 10), bg='lightblue').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self, textvariable=self.email_var, width=20, font=("Helvetica", 11))
        self.email_entry.grid(row=0, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Password: ", font=("Helvetica", 10), bg='lightblue').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, width=20, font=("Helvetica", 11))
        self.password_entry.grid(row=1, column=1, columnspan=4, sticky=tk.NSEW, pady=5)
        tk.Button(self, text="Generate").grid(row=1, column=5, sticky=tk.W, pady=5, padx=5)

        tk.Label(self, text="EPassword: ", font=("Helvetica", 10), bg='lightblue').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_password_var = tk.StringVar()
        self.email_password_entry = ttk.Entry(self, textvariable=self.email_password_var, width=20, font=("Helvetica", 11))
        self.email_password_entry.grid(row=2, column=1, columnspan=4, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="First Name: ", font=("Helvetica", 10), bg='lightblue').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(self, textvariable=self.first_name_var, width=9, font=("Helvetica", 11))
        self.first_name_entry.grid(row=3, column=1, sticky=tk.NSEW, pady=5)

        tk.Label(self, text="Last Name: ", font=("Helvetica", 10), bg='lightblue').grid(row=3, column=3, sticky=tk.N, pady=5)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(self, textvariable=self.last_name_var, width=9, font=("Helvetica", 11))
        self.last_name_entry.grid(row=3, column=4, sticky=tk.NSEW, pady=5)

        tk.Button(self, text="Submit", font=("Helvetica", 10)).grid(row=4, column=1, sticky=tk.NSEW, pady=15)
        tk.Button(self, text=" Cancel ", font=("Helvetica", 10)).grid(row=4, column=3, sticky=tk.NSEW, pady=15, padx=20)

    def on_close(self):
        self.destroy()
        self.is_open = False

import tkinter as tk
from tkinter import ttk


class FBManager(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Facebook Service")
        self.geometry("800x600")
        self.is_open = True
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.fb_account_list = FBAccountsList(self)

        button_frame = tk.Frame(self)
        button_frame.pack(padx=5, pady=20, anchor=tk.NW)
        button_add = tk.Button(button_frame, text="ADD", width=10, height=2, command=self.fb_account_list.show_selected)
        button_add.grid(row=0, column=0, padx=5)
        button_refresh = tk.Button(button_frame, text="REFRESH", width=10, height=2)
        button_refresh.grid(row=0, column=1, padx=5)
        button_remove = tk.Button(button_frame, text="REMOVE", width=10, height=2)
        button_remove.grid(row=0, column=2, padx=5)
        button_action = tk.Button(button_frame, text="RUN TASK", width=10, height=2)
        button_action.grid(row=0, column=3, padx=5)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Treeview', rowheight=25)
        self.fb_account_list.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def on_close(self):
        self.destroy()
        self.is_open = False


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


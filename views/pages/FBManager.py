import tkinter as tk
from tkinter import ttk


class FBManager(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title("Facebook Service")
        self.geometry("800x600")
        self.is_open = True
        button_frame = tk.Frame(self)
        button_frame.pack(padx=5, pady=20, anchor=tk.NW)
        button_add = tk.Button(button_frame, text="ADD", width=10, height=2)
        button_add.grid(row=0, column=0, padx=5)
        button_refresh = tk.Button(button_frame, text="REFRESH", width=10, height=2)
        button_refresh.grid(row=0, column=1, padx=5)
        button_remove = tk.Button(button_frame, text="REMOVE", width=10, height=2)
        button_remove.grid(row=0, column=2, padx=5)
        button_action = tk.Button(button_frame, text="RUN TASK", width=10, height=2)
        button_action.grid(row=0, column=3, padx=5)

        self.fb_accounts = ttk.Treeview(self,
                                        columns=("ID", "email", "password", "device", "status", "action"),
                                        show="headings")
        self.fb_accounts.heading("ID", text="ID")
        self.fb_accounts.heading("email", text="Email")
        self.fb_accounts.heading("password", text="Password")
        self.fb_accounts.heading("device", text="Device")
        self.fb_accounts.heading("status", text="Status")
        self.fb_accounts.heading("action", text="Action")

        self.fb_accounts.column("ID", width=10, anchor='center')
        self.fb_accounts.column("email", width=120, anchor='center')
        self.fb_accounts.column("password", width=80, anchor='center')
        self.fb_accounts.column("device", width=120, anchor='center')
        self.fb_accounts.column("status", width=50, anchor='center')
        self.fb_accounts.column("action", width=50, anchor='center')

        data = [
            (0, 'nct031194@icloud.com', '272337839', 'IMEI: 123124512512', 'Offline'),
            (1, 'nct031194@icloud.com', '272337839', 'IMEI: 123124512512', 'Offline'),
            (2, 'nct031194@icloud.com', '272337839', 'IMEI: 123124512512', 'Offline'),
        ]

        for i, (ID, email, password, device, status) in enumerate(data):
            item_id = self.fb_accounts.insert("", "end",
                                              values=(ID, email, password, device, status))
            self.fb_accounts.item(item_id, tags=(f'item{i}', 'unchecked'))

        self.fb_accounts.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())

    def on_close(self):
        self.destroy()
        self.is_open = False

    def on_treeview_select(self, event):
        selected_item = event.selection()
        if selected_item:
            values = self.fb_accounts.item(selected_item, 'values')
            print("Selected Row:", selected_item)
            print("Values:", values)

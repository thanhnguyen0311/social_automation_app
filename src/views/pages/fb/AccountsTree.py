import tkinter as tk
from tkinter import ttk
import threading
import time

from src.services.fbService import get_all_fb_accounts, remove_fb_accounts


class FBAccountsList(ttk.Treeview):
    def __init__(self, master):
        ttk.Treeview.__init__(self, master,
                              columns=("ID", "Name", "email", "password",
                                       "device", "status", "last_login",
                                       "create_date", "live"),
                              show="headings", selectmode="extended")
        self.hint_window = None
        self.refresh_thread = threading.Thread(target=self.refresh)
        self.refresh_thread.start()
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
        self.column("device", width=70, anchor='center')
        self.column("status", width=50, anchor='center')
        self.column("last_login", width=50, anchor='center')
        self.column("create_date", width=50, anchor='center')
        self.column("live", width=80, anchor='center')

        self.bind("<Motion>", self.on_cursor_move)
        self.data = {}

    def get_selected(self):
        list_account = []
        for item in self.selection():
            list_account.append(self.data[item])

        return list_account

    def on_cursor_move(self, event):
        if self.hint_window:
            self.hint_window.destroy()

        col = self.identify_column(event.x)
        item_iid = self.identify_row(event.y)
        if col == '#5':
            if item_iid and self.data[int(item_iid)].device:
                self.show_device_hint(event, self.data[int(item_iid)])

    def remove_accounts(self):
        for item in self.selection():
            if remove_fb_accounts(item) is True:
                print("Deleted account id {0}".format(item))
        self.on_refresh_clicked()

    def on_refresh_clicked(self):
        self.refresh_thread = threading.Thread(target=self.refresh, daemon=True)
        self.refresh_thread.start()

    def refresh(self):
        self.delete(*self.get_children())
        self.data = get_all_fb_accounts(1)
        for account_id, account in self.data.items():
            if account.is_deleted:
                continue

            device_imei = ""
            if account.device:
                device_imei = account.device.imei

            self.insert("", "end", iid=account.facebook_account_id,
                        values=(account.facebook_account_id,
                                account.first_name + " " + account.last_name,
                                account.email.email_address,
                                account.password,
                                device_imei,
                                "",
                                account.last_login,
                                account.create_date,
                                ""))

            bbox = self.bbox(account_id, "status")
            x, y, width, height = bbox
            if account.status == "ALIVE":
                account.status = tk.Label(self, text="LIVE", fg="green")
                account.status.place(x=x, y=y, width=width, height=height)

        self.data[2].status.config(text="TEST")

    def show_device_hint(self, event, account):
        self.hint_window = tk.Toplevel(self, highlightthickness=2, highlightbackground="gray")
        self.hint_window.wm_overrideredirect(True)
        self.hint_window.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        tk.Label(self.hint_window, text="IMEI").grid(row=0, column=0, sticky=tk.W)
        tk.Label(self.hint_window, text=account.device.imei).grid(row=0, column=1, sticky=tk.NW)
        tk.Label(self.hint_window, text="Manufacturer").grid(row=1, column=0, sticky=tk.W)
        tk.Label(self.hint_window, text=account.device.manufacturer).grid(row=1, column=1, sticky=tk.NW)
        tk.Label(self.hint_window, text="Model").grid(row=2, column=0, sticky=tk.W)
        tk.Label(self.hint_window, text=account.device.model).grid(row=2, column=1, sticky=tk.NW)
        tk.Label(self.hint_window, text="IMSI").grid(row=3, column=0, sticky=tk.W)
        tk.Label(self.hint_window, text=account.device.imsi).grid(row=3, column=1, sticky=tk.NW)
        tk.Label(self.hint_window, text="Android ID").grid(row=4, column=0, sticky=tk.W)
        tk.Label(self.hint_window, text=account.device.androidId).grid(row=4, column=1, sticky=tk.NW)
        tk.Label(self.hint_window, text="Sim Serial").grid(row=5, column=0, sticky=tk.W)
        tk.Label(self.hint_window, text=account.device.simSerial).grid(row=5, column=1, sticky=tk.NW)
        tk.Label(self.hint_window, text="Mac Address").grid(row=6, column=0, sticky=tk.W)
        tk.Label(self.hint_window, text=account.device.macAddress).grid(row=6, column=1, sticky=tk.NW)

import tkinter as tk
from tkinter import ttk
import threading
from tkinter import font

from src.models.Facebook import FBAccount
from src.services.fbService import get_all_fb_accounts, remove_fb_accounts
from src.views.pages.fb.EditPopup import EditFacebookAccount


class FBAccountsList(ttk.Treeview):
    def __init__(self, master, show_checkpoint, show_insecure):
        ttk.Treeview.__init__(self, master, columns=("ID", "Name", "email",
                                                     "device", "last_login",
                                                     "create_date", "live", "status"),
                              show="headings", selectmode="extended")
        self.hint_window = None
        self.show_checkpoint = show_checkpoint
        self.show_insecure = show_insecure
        self.is_loaded = True
        self.refresh_thread = threading.Thread(target=self.refresh)
        self.refresh_thread.start()
        self.edit_popup = None
        self.heading("ID", text="ID")
        self.heading("Name", text="Name")
        self.heading("email", text="Email")
        self.heading("device", text="Device")
        self.heading("last_login", text="Last login")
        self.heading("create_date", text="Create date")
        self.heading("live", text="Live Record")
        self.heading("status", text="Status")

        self.column("ID", width=5, anchor='center')
        self.column("Name", width=50, anchor='center')
        self.column("email", width=120, anchor='center')
        self.column("device", width=70, anchor='center')
        self.column("last_login", width=50, anchor='center')
        self.column("create_date", width=50, anchor='center')
        self.column("live", width=80, anchor='center')
        self.column("status", width=20, anchor='center')

        self.bind("<Motion>", self.on_cursor_move)

        self.bind("<Double-1>", self.on_double_click)

    def get_selected(self):
        list_account = []
        for item in self.selection():
            list_account.append(FBAccount.list_accounts[int(item)])

        return list_account

    def on_double_click(self, event):
        item_iid = self.selection()[0]
        account = FBAccount.list_accounts[int(item_iid)]
        print(account)
        if self.edit_popup is None or self.edit_popup.is_open is False:
            self.edit_popup = EditFacebookAccount(self, account_iid=item_iid)

    def on_cursor_move(self, event):
        if self.is_loaded:
            if self.hint_window:
                self.hint_window.destroy()

            col = self.identify_column(event.x)
            item_iid = self.identify_row(event.y)
            if col == '#4':
                if item_iid and FBAccount.list_accounts[int(item_iid)].device:
                    self.show_device_hint(event, FBAccount.list_accounts[int(item_iid)])

    def remove_accounts(self):
        for item in self.selection():
            if remove_fb_accounts(item) is True:
                print("Deleted account id {0}".format(item))
        self.on_refresh_clicked()

    def on_refresh_clicked(self):
        self.is_loaded = False
        if not self.refresh_thread.is_alive():
            self.refresh_thread = threading.Thread(target=self.refresh, daemon=True)
            self.refresh_thread.start()

    def refresh(self):
        FBAccount.list_accounts = get_all_fb_accounts(1)
        if self.winfo_exists():
            self.list_filter()

    def show_device_hint(self, event, account):
        self.hint_window = tk.Toplevel(self, highlightthickness=2, highlightbackground="gray")
        self.hint_window.wm_overrideredirect(True)
        self.hint_window.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        tk.Label(self.hint_window,
                 text="IMEI").grid(row=0, column=0, sticky=tk.W)
        tk.Label(self.hint_window,
                 text=account.device.imei).grid(row=0, column=1, sticky=tk.NW)
        tk.Label(self.hint_window,
                 text="Manufacturer").grid(row=1, column=0, sticky=tk.W)
        tk.Label(self.hint_window,
                 text=account.device.manufacturer).grid(row=1, column=1, sticky=tk.NW)
        tk.Label(self.hint_window,
                 text="Model").grid(row=2, column=0, sticky=tk.W)
        tk.Label(self.hint_window,
                 text=account.device.model).grid(row=2, column=1, sticky=tk.NW)
        tk.Label(self.hint_window,
                 text="IMSI").grid(row=3, column=0, sticky=tk.W)
        tk.Label(self.hint_window,
                 text=account.device.imsi).grid(row=3, column=1, sticky=tk.NW)
        tk.Label(self.hint_window,
                 text="Android ID").grid(row=4, column=0, sticky=tk.W)
        tk.Label(self.hint_window,
                 text=account.device.androidId).grid(row=4, column=1, sticky=tk.NW)
        tk.Label(self.hint_window,
                 text="Sim Serial").grid(row=5, column=0, sticky=tk.W)
        tk.Label(self.hint_window,
                 text=account.device.simSerial).grid(row=5, column=1, sticky=tk.NW)
        tk.Label(self.hint_window,
                 text="Mac Address").grid(row=6, column=0, sticky=tk.W)
        tk.Label(self.hint_window,
                 text=account.device.macAddress).grid(row=6, column=1, sticky=tk.NW)

    def list_filter(self):

        self.delete(*self.get_children())

        for ID, (account_id, account) in enumerate(FBAccount.list_accounts.items(), start=1):

            if self.show_insecure.get():
                if account.secure:
                    continue
            if not self.show_checkpoint.get():
                if account.status == "CHECKPOINT":
                    continue
            if account.is_deleted:
                continue

            email_address = account.email.email_address
            if account.secure:
                email_address = account.email.email_address + " ✔️"

            device_imei = ""
            if account.device:
                device_imei = account.device.imei

            self.insert("", "end", iid=account.facebook_account_id,
                        values=(ID,
                                account.first_name + " " + account.last_name,
                                email_address,
                                device_imei,
                                account.last_login,
                                account.create_date,
                                "",
                                account.status
                                ))

        self.is_loaded = True

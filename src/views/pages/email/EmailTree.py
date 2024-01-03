import tkinter as tk
from tkinter import ttk
import threading
from tkinter import font

from src.services.emailService import get_all_emails, remove_email


class MailList(ttk.Treeview):
    def __init__(self, master):
        ttk.Treeview.__init__(self, master,
                              columns=("ID", "name",
                                       "email", "device",
                                       "create_date",
                                       "facebook", "tiktok",
                                       "telegram", "status"),
                              show="headings", selectmode="extended")
        self.refresh_thread = threading.Thread(target=self.refresh)
        self.refresh_thread.start()
        self.hint_window = None
        self.data = {}
        self.bbox_list = {}
        self.bind("<Motion>", self.on_cursor_move)
        self.heading("ID", text="ID")
        self.heading("name", text="Name")
        self.heading("email", text="Email")
        self.heading("device", text="Device")
        self.heading("create_date", text="Create date")
        self.heading("facebook", text="Facebook")
        self.heading("tiktok", text="Tiktok")
        self.heading("telegram", text="Telegram")
        self.heading("status", text="Status")

        self.column("ID", width=3, anchor='center')
        self.column("name", width=60, anchor='center')
        self.column("email", width=80, anchor='center')
        self.column("device", width=40, anchor='center')
        self.column("create_date", width=40, anchor='center')
        self.column("facebook", width=3, anchor='center')
        self.column("tiktok", width=3, anchor='center')
        self.column("telegram", width=3, anchor='center')
        self.column("status", width=10, anchor='center')

    def refresh(self):
        self.delete(*self.get_children())
        self.data = get_all_emails(1)
        for id, (email_id, email) in enumerate(self.data.items(), start=1):
            if self.bbox_list.get(email_id):
                self.bbox_list.get(email_id).destroy()
            else:
                pass

            if email.is_deleted:
                continue

            device_imei = ""
            if email.device:
                device_imei = email.device.imei

            self.insert("", "end", iid=email_id,
                        values=(id,
                                email.first_name + " " + email.last_name,
                                email.email_address,
                                device_imei,
                                email.create_date,
                                "X" if email.facebook else "",
                                "X" if email.tiktok else "",
                                "X" if email.telegram else "",
                                email.status
                                ))
        self.show_status()

    def on_refresh_clicked(self):
        self.refresh_thread = threading.Thread(target=self.refresh, daemon=True)
        self.refresh_thread.start()

    def show_status(self):
        for email_id, email in self.data.items():
            bbox = self.bbox(email_id, "status")
            x, y, width, height = bbox
            if email.status == "REGISTERED":
                bold_font = font.Font(family="Arial", size=8, weight="bold")
                email.status = tk.Label(self, text="REGISTERED", bg='white', fg='blue', font=bold_font)
                email.status.place(x=x, y=y, width=width, height=height)

            if email.status == "ALIVE":
                bold_font = font.Font(family="Arial", size=8, weight="bold")
                email.status = tk.Label(self, text="LIVE", bg='white', fg='green', font=bold_font)
                email.status.place(x=x, y=y, width=width, height=height)

            if email.status == "CHECKPOINT":
                bold_font = font.Font(family="Arial", size=8, weight="bold")
                email.status = tk.Label(self, text="CHECKPOINT", bg='white', fg='red', font=bold_font)
                email.status.place(x=x, y=y, width=width, height=height)

            if email.status == "DIE":
                bold_font = font.Font(family="Arial", size=8, weight="bold")
                email.status = tk.Label(self, text="DIE", bg='white', fg='black', font=bold_font)
                email.status.place(x=x, y=y, width=width, height=height)
            self.bbox_list[email_id] = email.status

    def on_cursor_move(self, event):
        if self.hint_window:
            self.hint_window.destroy()

        col = self.identify_column(event.x)
        item_iid = self.identify_row(event.y)
        if col == '#4':
            if item_iid and self.data[int(item_iid)].device:
                self.show_device_hint(event, self.data[int(item_iid)])

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

    def get_selected(self):
        list_email = []
        for item in self.selection():
            list_email.append(self.data[int(item)])

        return list_email

    def remove_accounts(self):
        for item in self.selection():
            if remove_email(item) is True:
                print("Deleted account id {0}".format(item))
        self.on_refresh_clicked()

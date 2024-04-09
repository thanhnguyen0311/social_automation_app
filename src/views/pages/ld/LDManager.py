import time
import tkinter as tk

from src.ld_manager.get_list_ld import get_list_ld
from src.ld_manager.quit_ld import quit_all, quit_ld
from src.ld_manager.reboot_ld import reboot_ld
from src.ld_manager.remove_ld import remove_ld
from src.ld_manager.run_ld import run_ld
from src.ld_manager.sort_ld import sort_ld
from src.models.Facebook import FBAccount
from src.models.ListDevices import ListDevices
from src.services.deviceService import create_device


class LDManager_Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.menu_bar = tk.Frame(self)
        self.menu_bar.grid(row=1, column=0, sticky="w", padx=5)
        self.button_add = tk.Button(self.menu_bar, text="Add", width=10, height=2, command=create_device)
        self.button_add.grid(row=0, column=0, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="Refresh", width=10, height=2, command=self.refresh)
        self.button_get.grid(row=0, column=1, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="Remove All", width=10, height=2, command=self.remove_all)
        self.button_get.grid(row=0, column=2, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="Kill All", width=10, height=2, command=self.kill_all)
        self.button_get.grid(row=0, column=3, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="Run All", width=10, height=2, command=self.run_all)
        self.button_get.grid(row=0, column=4, padx=5, pady=5)
        self.button_get = tk.Button(self.menu_bar, text="Sort View", width=10, height=2, command=sort_ld)
        self.button_get.grid(row=0, column=5, padx=5, pady=5)
        self.titles = tk.Label(self, text="Devices")
        self.titles.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        self.device_list = tk.Frame(self)
        self.refresh()

    def device_frame(self):
        self.device_list.grid(row=3, column=0, sticky="w", padx=0)
        tk.Label(self.device_list, text="ID").grid(row=0, column=0, sticky="w", padx=20, pady=5)
        tk.Label(self.device_list, text="Name").grid(row=0, column=1, sticky="news", padx=30, pady=5)
        tk.Label(self.device_list, text="IMEI").grid(row=0, column=2, sticky="news", padx=40, pady=5)
        tk.Label(self.device_list, text="UUID").grid(row=0, column=3, sticky="news", padx=40, pady=5)
        tk.Label(self.device_list, text="Status").grid(row=0, column=4, sticky="w", padx=15, pady=5)

    def refresh(self):
        # ListDevices.add_task(Task(function=get_list_ld, name="GET ALL DEVICES"))
        get_list_ld()
        time.sleep(2)
        if not ListDevices.is_running:
            self.device_list.destroy()
            self.device_list = tk.Frame(self)
            self.device_frame()
            for row, (key, value) in enumerate(ListDevices.ld_list.items(), start=1):
                self.device_line(row, value)

    def device_line(self, row, device):
        tk.Label(self.device_list, text=row).grid(row=row, column=0)
        tk.Label(self.device_list, text=device.name).grid(row=row, column=1, sticky="news")
        tk.Label(self.device_list, text=device.imei).grid(row=row, column=2, sticky="news")
        tk.Label(self.device_list, text=device.uuid).grid(row=row, column=3, sticky="news")
        check = False
        if check:
            tk.Label(self.device_list, text="• Active", fg="green").grid(row=row, column=4)
        else:
            tk.Label(self.device_list, text="Offline", fg="gray").grid(row=row, column=4)

        tk.Button(self.device_list, text="Kill", command=lambda: quit_ld(device)).grid(row=row, column=5)
        tk.Button(self.device_list, text="Run", command=lambda: run_ld(device)).grid(row=row, column=6)
        tk.Button(self.device_list, text="Remove", command=lambda: (remove_ld(device)
                                                                    , self.refresh())).grid(row=row, column=7)
        tk.Button(self.device_list, text="Reload", command=lambda: reboot_ld(device)).grid(row=row, column=8)

    def add_device(self):
        pass

    def remove_all(self):
        # remove_all_ld()
        self.refresh()

    def kill_all(self):
        quit_all()
        self.refresh()

    def run_all(self):
        return

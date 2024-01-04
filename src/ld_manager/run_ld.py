import subprocess
import sys
import os
import threading
import time

from src.constants.constants import LDCONSOLE_PATH
from src.ld_manager.adb_shells import restart_adb_server
from src.ld_manager.is_running import is_running
from src.ld_manager.reboot_ld import reboot_ld

from src.services.deviceService import check_device_exists

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def run_ld(device):
    try:
        subprocess.call([LDCONSOLE_PATH] + ["launch"] + ["--name"] + [device.name], shell=True)
        time.sleep(1)
        subprocess.run(["adb", "kill-server"], check=True)
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def run_list_ld(list_selected):
    try:
        restart_adb_server()
        list_devices = []
        for account in list_selected:
            if account.device is None:
                check_devices(account, list_devices)
                continue
            threading.Thread(target=check_devices, args=(account, list_devices,)).start()
        while len(list_devices) != len(list_selected):
            if len(list_devices) == len(list_selected):
                break
        check_devices_ready(list_devices)
        return list_selected

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def check_devices(account, list_devices):
    account.device = check_device_exists(account)
    if not is_running(account.device):
        run_ld(account.device)
    list_devices.append(account.device)


def check_devices_ready(list_devices):
    try:
        check = False
        while not check:
            check = True
            time.sleep(30)
            result = subprocess.run(["adb", "devices"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
            lines = result.stdout.split('\n')
            list_devices_adb = {}
            for line in lines:
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) == 2:
                        emulator, status = parts
                        list_devices_adb[emulator.strip()] = status.strip()
            for device in list_devices:
                try:
                    if list_devices_adb[device.uuid] == "offline":
                        # if is_running(device):
                        #     reboot_ld(device)
                        # else:
                        #     run_ld(device)
                        # restart_adb_server()
                        time.sleep(60)
                        check = False

                except KeyError:
                    # if is_running(device):
                    #     reboot_ld(device)
                    # else:
                    #     run_ld(device)
                    # restart_adb_server()
                    time.sleep(60)
                    check = False
            if check:
                break
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


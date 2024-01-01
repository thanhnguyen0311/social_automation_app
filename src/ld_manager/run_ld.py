import subprocess
import sys
import os
import time

from src.constants.constants import LDCONSOLE_PATH
from src.ld_manager.is_running import is_running
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

        time.sleep(5)
        subprocess.run(["adb", "kill-server"], check=True)
        time.sleep(5)
        subprocess.run(["adb", "start-server"], check=True)
        time.sleep(10)
        list_account = list_selected
        for account in list_account:
            account.device = check_device_exists(account)
            if is_running(account.device) is False:
                run_ld(account.device)
        time.sleep(15)
        return list_account

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return list_account

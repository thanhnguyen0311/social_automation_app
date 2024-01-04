import subprocess
import sys
import os
import time

from src.constants.constants import LDCONSOLE_PATH

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def restart_adb_server():
    try:
        time.sleep(5)
        subprocess.run(["adb", "kill-server"], check=True)
        time.sleep(5)
        subprocess.run(["adb", "start-server"], check=True)
        time.sleep(5)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def find_package_running(package, device):
    packages = []
    try:
        result = subprocess.run(
            [LDCONSOLE_PATH] + ["adb", "--name", device.name, "--command", "shell pm list packages"]
            , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True)
        packages = result.stdout.split('\n')
        for pkg in packages:
            if pkg.strip() == f'package:{package}':
                return True

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

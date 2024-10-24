import subprocess
import sys
import os
from src.constants.constants import LDCONSOLE_PATH

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def remove_ld(device):
    try:
        subprocess.run([LDCONSOLE_PATH] + ["remove", "--name", device.name], shell=True)
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def remove_all_ld(ld_list):
    for key, device in ld_list.items():
        try:
            subprocess.run([LDCONSOLE_PATH] + ["remove", "--name", device.name], shell=True)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

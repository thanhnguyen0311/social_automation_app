import subprocess
import sys
import os
import time

from src.constants.constants import LDCONSOLE_PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def run_ld(device):
    try:
        subprocess.call([LDCONSOLE_PATH] + ["launch"] + ["--name"] + [device.name], shell=True)
        time.sleep(1)
        subprocess.run(["adb", "start-server"], check=True)
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

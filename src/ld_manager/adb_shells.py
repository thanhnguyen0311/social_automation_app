import subprocess
import sys
import os
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def restart_adb_server():
    try:
        time.sleep(2)
        subprocess.run(["adb", "kill-server"], check=True)
        time.sleep(2)
        subprocess.run(["adb", "start-server"], check=True)
        time.sleep(2)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


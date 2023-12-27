import subprocess
import sys
import os
from src.constants.constants import LDCONSOLE_PATH

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def is_running(device):
    try:
        result = subprocess.run([LDCONSOLE_PATH] + ["isrunning"] + ["--index"] + [str(device.ID)], shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout

            if output == "running":
                return True
            if output == "stop":
                return False
        else:
            print("Command failed with return code:", result.returncode)
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

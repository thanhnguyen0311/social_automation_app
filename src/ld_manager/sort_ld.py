import subprocess
import sys
import os
from src.constants.constants import LDCONSOLE_PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def sort_ld():
    try:
        subprocess.call([LDCONSOLE_PATH] + ["sortWnd"], shell=True)
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

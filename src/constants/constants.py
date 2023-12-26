import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

LDPLAYER_PATH = "D:\LDPlayer\LDPlayer9"
LDCONSOLE_PATH = os.path.join(LDPLAYER_PATH, "ldconsole.exe")
CLONE_LD_DATA = True
LOGO_PATH = os.path.join("assets", "img", "logo.png")

account_data_config = {
    'host': '125.212.243.130',
    'user': 'nct031194',
    'password': '272337839',
    'database': 'social_automation',
}

import threading
import time

from src.remote.email.register import register_email
from src.services.deviceService import run_account_devices


class EmailTask:
    @staticmethod
    def create_emails(list_account):
        run_account_devices(list_account)
        for account in list_account:
            account.device.thread = threading.Thread(target=register_email, args=(account,))
            account.device.thread.start()
            account.device.is_running = True
            time.sleep(1)

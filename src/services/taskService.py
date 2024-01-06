import threading
import time

from src.remote.email.register import register_email
from src.remote.facebook.farm.newfeed import farm_newFeed
from src.remote.facebook.login import login_facebook
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


class FacebookTask:
    @staticmethod
    def login(list_account):
        run_account_devices(list_account)
        for account in list_account:
            account.device.thread = threading.Thread(target=login_facebook, args=(account,))
            account.device.thread.start()
            account.device.is_running = True
            time.sleep(1)

    @staticmethod
    def farm_new_feed(list_account):
        run_account_devices(list_account)
        for account in list_account:
            account.device.thread = threading.Thread(target=farm_newFeed, args=(account,))
            account.device.thread.start()
            account.device.is_running = True
            time.sleep(1)

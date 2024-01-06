import threading
import time

from src.models.tasks.Task import Task
from src.remote.facebook.farm.newfeed import FarmNewFeed
from src.remote.facebook.login import LoginFacebook
from src.services.deviceService import run_account_devices


class FacebookTask(Task):
    def __init__(self, function, args, list_account, name):
        super().__init__(function, args, list_account, name)

    def login(self):
        run_account_devices(self.list_account)
        for account in self.list_account:
            account.task = LoginFacebook(account)
            account.device.thread = threading.Thread(target=account.task.__run__)
            account.device.thread.start()
            time.sleep(1)

    def farm_new_feed(self):
        run_account_devices(self.list_account)
        for account in self.list_account:
            account.task = FarmNewFeed(account)
            account.device.thread = threading.Thread(target=account.task.__run__)
            account.device.thread.start()
            account.device.is_running = True
            time.sleep(1)



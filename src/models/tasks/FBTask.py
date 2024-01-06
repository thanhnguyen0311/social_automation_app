import threading
import time

from src.models.tasks.Task import Task
from src.remote.facebook.farm.newfeed import FarmNewFeed
from src.remote.facebook.login import LoginFacebook
from src.remote.facebook.register import RegisterFacebook
from src.services.deviceService import run_account_devices


class FacebookTask(Task):
    def __init__(self, function, args, list_account, name):
        super().__init__(function, args, list_account, name)

    def _run_task(self, task_creator):
        run_account_devices(self.list_account)
        for account in self.list_account:
            account.task = task_creator(account)
            account.device.thread = threading.Thread(target=account.task.__run__)
            account.device.thread.start()
            time.sleep(1)

    def login(self):
        self._run_task(LoginFacebook)

    def farm_new_feed(self):
        self._run_task(FarmNewFeed)

    def register(self):
        self._run_task(RegisterFacebook)


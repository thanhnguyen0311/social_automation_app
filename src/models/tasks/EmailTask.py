import threading
import time

from src.models.tasks.Task import Task
from src.remote.email.register import RegisterEmail
from src.services.deviceService import run_account_devices


class EmailTask(Task):
    def __init__(self, function, args, list_account, name):
        super().__init__(function, args, list_account, name)

    def _run_task(self, task_creator):
        run_account_devices(self.list_account)
        for account in self.list_account:
            account.task = task_creator(account)
            account.device.thread = threading.Thread(target=account.task.__run__)
            account.device.thread.start()
            time.sleep(1)

    def create_emails(self):
        self._run_task(RegisterEmail)

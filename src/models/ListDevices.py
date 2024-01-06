import queue
import threading
import time


class ListDevices:
    ld_list = {}
    tasks = queue.Queue()
    thread = None
    is_running = False
    running_task = None

    @staticmethod
    def add_task(task):
        ListDevices.tasks.put(task)
        ListDevices.is_running = True
        if ListDevices.thread is None or not ListDevices.thread.is_alive():
            ListDevices.thread = threading.Thread(target=ListDevices._worker)
            ListDevices.thread.start()
            print("ListDevices.thread started")

    @staticmethod
    def _worker():
        while ListDevices.is_running:
            if not ListDevices.tasks.empty():
                task = ListDevices.tasks.get()
                if task.name is not None:
                    print(f"Executing task: {task.name}")
                task.execute()
                ListDevices.running_task = task
                while task.is_running:
                    if not task.is_running:
                        ListDevices.running_task = None
                        break

            else:
                time.sleep(1)
                break
        ListDevices.is_running = False
        print("Done all ListDevices tasks")

    @staticmethod
    def cancel_current_task():
        if ListDevices.running_task is not None:
            if ListDevices.running_task.is_running:
                print(f"cancel task : {ListDevices.running_task.name}")
                ListDevices.running_task.__stop__()

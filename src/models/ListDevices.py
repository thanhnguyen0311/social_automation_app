import queue
import threading
import time


class ListDevices:
    ld_list = {}
    tasks = queue.Queue()
    thread = None
    is_running = False

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
            else:
                time.sleep(1)
                break
        ListDevices.is_running = False
        print("Done all ListDevices tasks")



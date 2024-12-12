from dataclasses import dataclass
from queue import Queue
from threading import Thread


@dataclass
class Task:
    key: str = None
    value: str = None
    response_queue: Queue = None
    response: str = None


class TaskProcessor(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._queue = Queue()
        self._data = dict()

    def process(self, task):
        self._queue.put(task)

    def run(self):
        while True:
            try:
                task = self._queue.get()
                try:
                    if task is not None:
                        if task.key is not None and task.value is not None:
                            self._data[task.key] = task.value
                            task.response = "OK"
                        elif task.key is not None and task.value is None:
                            task.response = self._data[task.key]
                        else:
                            task.response = "ERR Task Processor: key is None"
                except KeyError:
                    task.response = ""
                except Exception as e:
                    task.response = f"ERR Task Processor: {e}"
                finally:
                    task.response_queue.put(task)
            except KeyboardInterrupt:
                break


class QueueDataStore:
    def __init__(self):
        self.processor = TaskProcessor()
        self.processor.start()
        self.result_queue = Queue()

    def get(self, key):
        task = Task(key=key, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

    def set(self, key, value):
        task = Task(key=key, value=value, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

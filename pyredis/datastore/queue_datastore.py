from dataclasses import dataclass
from queue import Queue
from threading import Thread
from .data import Data
import datetime


@dataclass
class Task:
    command: str = None
    key: str = None
    value: Data = None
    response_queue: Queue = None
    response: str = None


class TaskProcessor(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._queue = Queue()
        self._data = dict()
        self._keys_with_expiry = list()

    def process(self, task):
        self._queue.put(task)

    def run(self):
        while True:
            try:
                task = self._queue.get()
                try:
                    if task is not None:
                        if task.key is None:
                            task.response = "ERR Task Processor: key is None"
                            break

                        self._check_expiry(task.key)

                        if task.value is None:
                            if task.command == "GET":
                                task.response = self._data[task.key]
                            if task.command == "DEL":
                                if task.key in self._keys_with_expiry:
                                    self._keys_with_expiry.remove(task.key)
                                del self._data[task.key]
                                task.response = "OK"
                        else:
                            self._data[task.key] = task.value
                            if task.value.expiry is not None:
                                self._add_expiry(task.key)
                            task.response = "OK"
                except KeyError:
                    task.response = ""
                except Exception as e:
                    task.response = f"ERR Task Processor: {e}"
                finally:
                    task.response_queue.put(task)
            except KeyboardInterrupt:
                break

    def _check_expiry(self, key):
        if key in self._keys_with_expiry:
            expiry = self._data[key].expiry
            if expiry is not None and expiry <= datetime.datetime.now():
                del self._data[key]
                self._keys_with_expiry.remove(key)

    def _add_expiry(self, key):
        self._keys_with_expiry.append(key)


class QueueDataStore:
    def __init__(self):
        self.processor = TaskProcessor()
        self.processor.start()
        self.result_queue = Queue()

    def get(self, key):
        task = Task(command="GET", key=key, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

    def set(self, key, value):
        task = Task(command="SET", key=key, value=value, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

    def delete(self, key):
        task = Task(command="DEL", key=key, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

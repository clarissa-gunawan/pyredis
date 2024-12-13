from dataclasses import dataclass
from queue import Queue
from threading import Thread
from .data import Data
import datetime


@dataclass
class Task:
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
        # self._expiry = new dict(), or tuple, or datatype
        # filter( if datatype.expiry <= timestamp)
        # array of keys with expiries - random sample

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
                            task.response = self._data[task.key]
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
        task = Task(key=key, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

    def set(self, key, value):
        task = Task(key=key, value=value, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

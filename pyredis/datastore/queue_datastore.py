# from queue import Queue
# from threading import Thread

# @dataclass
# class Task:
#     command: str
#     key: str
#     value: str
#     response_queue: Queue
#     response: int = 0


# class TaskProcessor(Thread):
#     def __init__(self):
#         super().__init__(daemon=True)
#         self._queue = Queue()

#     def process(self, task):
#         self._queue.put(task)

#     def run(self):
#         while True:
#             task = self._queue.get()
#             if task is not None:
#                 task.response = task.val * 2
#                 task.response_queue.put(task)


class QueueDataStore:
    def __init__(self):
        pass


# class QueueDataStore(Thread):
#     def __init__(self):
#         super().__init__(daemon=True)
#         self._queue = Queue()
#         self._data = dict()

#     def process(self, task):
#         self._queue.put(task)


#     def run(self):
#         while True:
#             task = self._queue.get()
#             if task is not None:
#                 if task.command == "SET":
#                     self._data[task.key] = task.value
#                     task.response = "OK"
#                 else:
#                     task.response = self._data[task.key]
#                 task.response_queue.put(task)


# if __name__ == "__main__":
#     processor = TaskProcessor()
#     processor.start()

#     # client / user of the processor
#     result_queue = Queue()

#     while True:
#         try:
#             v = input("Enter a value> ")
#             processor.process(Task(int(v), result_queue))
#             result = result_queue.get()
#             print(result.response)
#         except KeyboardInterrupt:
#             print()
#             break

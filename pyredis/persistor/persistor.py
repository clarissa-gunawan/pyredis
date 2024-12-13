from threading import Thread
from queue import Queue
import os
from dataclasses import dataclass
from pyredis.commands import parse_command
from pyredis.protocol import Error


class Persistor:
    def __init__(self, datastore=None, filename=None):
        self._filepath = self.initialize_file(filename)
        self.processor = TaskFileProcessor(filepath=self._filepath, datastore=datastore)
        self.processor.start()
        self.result_queue = Queue()

    def initialize_file(self, filename):
        if filename is None:
            filename = "data.aof"

        directory_path = "tmp"
        file_path = f"{directory_path}/{filename}"

        # Create the directory
        try:
            os.mkdir(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        except FileExistsError:
            print(f"Directory '{directory_path}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Create the file
        try:
            with open(file_path, "x") as file:
                file.write("")
            print(f"File {file_path} created successfully.")
        except FileExistsError:
            print(f"File {file_path} already exists.")

        return file_path

    def write_command(self, command):
        task = TaskFile(text=command, response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response

    def read(self):
        task = TaskFile(response_queue=self.result_queue)
        self.processor.process(task)
        result = self.result_queue.get()
        return result.response


@dataclass
class TaskFile:
    text: str = None
    response_queue: Queue = None
    response: str = None


class TaskFileProcessor(Thread):
    def __init__(self, filepath, datastore):
        super().__init__(daemon=True)
        self._queue = Queue()
        self._filepath = filepath
        self._datastore = datastore

    def process(self, task):
        self._queue.put(task)

    def run(self):
        while True:
            try:
                task = self._queue.get()
                try:
                    if task.text is None:
                        buffer = b""
                        with open(self._filepath, "rb") as file:
                            while True:
                                data = file.read(4096)
                                if not data:
                                    break

                                buffer += data

                                while buffer:
                                    processed_data, size = parse_command(buffer, self._datastore)

                                    if processed_data is None:
                                        break

                                    if isinstance(processed_data, Error):
                                        task.response = "ERR corrupt AOF file"
                                        break

                                    buffer = buffer[size:]
                        task.response = "OK"
                    else:
                        # Write into file with append mode
                        with open(self._filepath, "ab") as file:
                            file.write(task.text)
                        task.response = "OK"
                except Exception as e:
                    task.response = f"ERR Task File Processor: {e}"
                finally:
                    task.response_queue.put(task)
            except KeyboardInterrupt:
                break

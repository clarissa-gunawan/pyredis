# import os
# import subprocess
# import time
# import threading
# import pyredis


# def test_persistance():
#     test_filepath = "tmp/test/persistance_test.aof"
#     port = str(6381)

#     if os.path.exists(test_filepath):
#         os.remove(test_filepath)

#     t = threading.Thread(
#         target=pyredis.main, kwargs={
#                   "port": port, "threaded": True,
#                   "persistance": True, "persistor_filepath": test_filepath}
#     )
#     t.start()
#     time.sleep(0.1)  # 100ms

#     assert os.path.exists(test_filepath) == True

#     res = subprocess.run(["redis-cli", "-p", port, "SET", "message_persistance", "Hello World"], stdout=subprocess.PIPE)
#     assert res.returncode == 0
#     assert res.stdout.decode("utf-8").strip() == "OK"

#     res = subprocess.run(["redis-cli", "-p", port, "GET", "message_persistance"], stdout=subprocess.PIPE)
#     assert res.returncode == 0
#     assert res.stdout.decode("utf-8").strip() == "Hello World"

#     t.join()

#     t2 = threading.Thread(
#         target=pyredis.main, kwargs={
#                       "port": port, "threaded": True,
#                       "persistance": True, "persistor_filepath": test_filepath}
#     )
#     t2.start()
#     time.sleep(0.1)  # 100ms

#     res = subprocess.run(["redis-cli", "-p", port, "GET", "message_persistance"], stdout=subprocess.PIPE)
#     assert res.returncode == 0
#     assert res.stdout.decode("utf-8").strip() == "Hello World"

#     t2.join()

#     if os.path.exists(test_filepath):
#         os.remove(test_filepath)

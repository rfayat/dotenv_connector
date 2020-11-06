"""Master script, kills the minon once its counter reaches a threshold value

Author: Romain Fayat, November 2020

"""
from dotenv_connector import DotEnvConnector
import os
import time
import signal

threshold = 1e2

if __name__ == "__main__":
    # Initialize the connector
    d = DotEnvConnector(".my_variables")
    if "counter" not in d:
        d["counter"] = str(0)
    counter = int(d["counter"])

    # Compare the value of counter from .my_variable to the threshold
    while counter < threshold:
        counter = int(d["counter"])
        print(f"Waiting for the counter to reach {threshold} (now: {counter})")
        time.sleep(0.01)

    # Kill the minion if it is running
    if d["status"] == "running":
        print("Killing the minion process")
        pid = int(d["PID"])
        os.kill(pid, signal.SIGINT)  # Equivalent to ctrl-c

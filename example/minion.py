"""Minion script, killed by master once a condition is met

Author: Romain Fayat, November 2020

"""
from dotenv_connector import DotEnvConnector
import time
import os

if __name__ == "__main__":
    # Initialize the connector and store a few parameters
    d = DotEnvConnector(".my_variables")
    d["PID"] = str(os.getpid())  # Used by the master to kill the minion
    d["counter"] = str(0)
    d["status"] = "running"  # Current status of the script

    try:
        while True:
            time.sleep(.1)
            current_value = d["counter"]
            d["counter"] = str(int(current_value) + 1)
            print(f"Counter value: {current_value}")
    except KeyboardInterrupt:
        print("Process interrupted")
    finally:
        d.pop("counter")  # remove the counter from .my_variables
        d["status"] = "finished"

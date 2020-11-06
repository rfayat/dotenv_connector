"""DotEnvConnector allows to connect a dict of strings to a .env file

Author: Romain Fayat, November 2020

"""
from typing import Dict
import dotenv
import inspect


class DotEnvConnector(Dict):
    "Object used to connect to a local .env file"

    def __init__(self, path=".env"):
        "Handle a dotenv file similarly to a dictionary."
        self.path = path  # Path to the dotenv file

        if not self.dotenv_exists:
            self.create_empty_dotenv()

        super().__init__(self.current_dotenv_values)

    @property
    def dotenv_exists(self):
        "Return True if the dotenv file exists, else False."
        return len(self.dotenv) != 0

    @property
    def dotenv(self):
        "Path to the dotenv file"
        return dotenv.find_dotenv(self.path)

    @property
    def current_dotenv_values(self):
        "Values currently stored in the dotenv as a dict"
        return dotenv.dotenv_values(self.dotenv)

    def create_empty_dotenv(self):
        "Create an empty dotenv file based on the path"
        with open(self.path, 'w') as _:
            pass

    def update_from_dotenv(self):
        "Update the current values from the dotenv file"
        # Current status of the dotenv file
        dotenv_values = self.current_dotenv_values

        # Remove the keys that are not in the dotenv
        for k in set(super().keys()) - set(dotenv_values):
            super().pop(k)

        # Update the values from the dotenv file
        super().update(dotenv_values)

    def write_to_dotenv(self):
        "Write the current values of self to the dotenv file"
        # Current status of the dotenv file
        dotenv_values = self.current_dotenv_values

        # Remove the keys that are not in the self
        for k in set(dotenv_values) - set(super().keys()):
            dotenv.unset_key(self.dotenv, k)

        # Update the values from self
        for k in super().keys():
            dotenv.set_key(self.dotenv, k, self[k])

    def update_from_dotenv_before(f):
        "Decorate a method to update self from the dotenv file before running"

        def g(self, *args, **kwargs):
            "Overwrite self from the dotenv file and run f"
            self.update_from_dotenv()
            return f(self, *args, **kwargs)

        return g

    def write_to_dotenv_after(f):
        "Decorate a method to update the dotenv file after running"

        def g(self, *args, **kwargs):
            "Run f and update the dotenv file"
            out = f(self, *args, **kwargs)
            self.write_to_dotenv()
            return out

        return g

    def synced_with_dotenv(f):
        "Decorate a method to keep the dotenv synced with self"

        def g(self, *args, **kwargs):
            "Update data from the dotenv, run f and update the dotenv file"
            self.update_from_dotenv()
            out = f(self, *args, **kwargs)
            self.write_to_dotenv()
            return out

        return g

    def copy(self, new_path=".env"):
        "Associate a copy of self with a dotenv file and return its connector"
        copied_dict = super().copy()
        new_connector = DotEnvConnector(new_path)
        # Overwrite the content of the newly created connector and return it
        new_connector.clear()
        new_connector.update(copied_dict)
        return new_connector

    # Decorate the required functions
    # Those which require to read and write dotenv
    for f in ["update", "__setitem__", "__delitem__", "pop", "popitem"]:
        vars()[f] = synced_with_dotenv(getattr(dict, f))

    # Those which require only to read the data from dotenv
    for f in ["__str__", "__repr__", "__iter__", "__le__", "__gt__", "__ge__",
              "__len__", "__lt__", "__ne__", "__eq__", "get", "items",
              "values"]:
        vars()[f] = update_from_dotenv_before(getattr(dict, f))

    # Those which require only to write data to dotenv
    for f in ["clear"]:
        vars()[f] = write_to_dotenv_after(getattr(dict, f))

    def __getitem__(self, key):
        """Read the values of the .env file if needed and return the item

        __getitem__ is called by other methods (e.g. update), to avoid having
        multiple reading of the file, we update self only if __getitem__ is
        being called at the module level

        """
        if inspect.stack()[1][3] == "<module>":
            self.update_from_dotenv()

        return dict.__getitem__(self, key)

# dotenv connector
This code is essentially a wrapper around some of the functionalities of [python-dotenv](https://pypi.org/project/python-dotenv/), allowing to easily interact with a text file containing environment variables (read / write). Rather than being focused on web development, it is intended to facilitate the sharing of variables between python processes.

## Installation
The installation can be done directly from the github repository (requires Python 3.6+):
```bash
$ pip install git+https://github.com/rfayat/dotenv_connector.git
```

## Example
**From a first python process**:

```python
>>> from dotenv_connector import DotEnvConnector
>>> shared_variables = DotEnvConnector("path/to/.env")  # An empty file is created if needed
>>> print(shared_variables)
{}
>>> shared_variables["my_key"] = "my_value"  
```

The file `path/to/.env` now has the following content:
```json
my_key="my_value"
```

We can then modify the file storing the variables from another python process (or using any other tool). For instance, **from a different python process**:
</div>

```python
>>> from dotenv_connector import DotEnvConnector
>>> shared_variables = DotEnvConnector("path/to/.env")  # An empty file is created if needed
>>> shared_variables
{'my_key': 'my_value'}
>>> shared_variables["my_key"] = "new_value"  
```

This new value can directly be accessed **from the first python process**:
```python
>>> shared_variables["my_key"]
new_value
```

## Use case
See the [example folder](example) for an example where a [master script](example/master.py) kills a [minion script](example/minion.py) based on the value of one of its variable.

## Future directions

**Done**
- [x] First working version of the code
- [x] Cleaner doc with examples
- [x] Setup instructions + setup.py

**Low-hanging fruits**
- [ ] Unit-testing
- [ ] Better input parsing (.env files only tolerate strings)

**Longer-term**
- [ ] Replace .env file by JSON
  - Nested dictionaries could be used
  - More flexible when it comes to the data type
  - The input parsing could be done directly by playing with the json loader/writer

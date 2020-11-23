"""Installation of dotenv_connector.

Author: Romain Fayat, November. 2020
"""
import os
from setuptools import setup


def read(fname):
    "Read a file in the current directory."
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="dotenv_connector",
    version="0.1",
    author="Romain Fayat",
    description="Easy interaction with a dotenv file",  # noqa E501
    install_requires=["python-dotenv"],
    packages=["dotenv_connector"],
    long_description=read('README.md')
)

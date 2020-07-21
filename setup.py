#!/bin/env python
# coidng: utf-8

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rcon',
    version='0.0.0-SNAPSHOT',
    descriotion='Python implementation of RCON',
    long_description=readme,
    author='tama@ttk1',
    author_email='tama@ttk1.net',
    url='https://github.com/ttk1/py-rcon',
    license=license,
    pakages=find_packages(exclude=('test',))
)

#!/bin/env python

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rcon',
    version='1.2.0',
    description='Python implementation of RCON',
    long_description=readme,
    author='tama@ttk1',
    author_email='tama@ttk1.net',
    url='https://github.com/ttk1/py-rcon',
    license=license,
    packages=find_packages(exclude=('test',)),
    entry_points={
        'console_scripts': [
            'rcon-shell = rcon.__main__:main',
            'rcon-gui = rcon.gui:main'
        ]
    }
)

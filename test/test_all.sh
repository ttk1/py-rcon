#!/bin/env bash

# run all tests and report coverages
python -m coverage run -m unittest discover
python -m coverage report

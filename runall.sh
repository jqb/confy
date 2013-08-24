#!/bin/bash

# simple utility to avoid typing the same command over and over again
tox && coverage erase && coverage run runtests.py && coverage html && coverage report

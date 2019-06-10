#!/bin/bash

virtualenv -p /usr/bin/python3 .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r test-requirements.txt
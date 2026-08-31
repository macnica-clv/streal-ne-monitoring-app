#!/bin/bash

APP_DIR="/opt/data/app/Hiz-mil"
PYTHON="/opt/data/python-runtime/python3"
PYTHON_HOME="/opt/data/python-runtime/usr"
PYTHON_PATH="/opt/data/python-runtime/usr/lib/python3/dist-packages"

cd "$APP_DIR" || exit 1

PYTHONHOME="$PYTHON_HOME" \
PYTHONPATH="$PYTHON_PATH" \
"$PYTHON" -u main_headless.py --console
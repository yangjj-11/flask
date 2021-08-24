#!/bin/bash
SERVICE=$1

export PRJ_ENV=dev
export PYTHONPATH=`pwd`

if [ x"$SERVICE" = x"format" ]; then
    isort flaskr/
    black flaskr/
elif [ x"$SERVICE" = x"flake" ]; then
    flake8 flaskr/
elif [ x"$SERVICE" = x"test" ]; then
    pytest tests/
fi

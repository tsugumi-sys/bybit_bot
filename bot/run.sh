#!/bin/bash

HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-5000}
APP_NAME=${APP_NAME:-"app:app"}

$(cd src && uvicorn ${APP_NAME} \
    --host ${HOST} \
    --port ${PORT})
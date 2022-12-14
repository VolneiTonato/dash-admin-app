#!/bin/bash

. .venv/bin/activate && \
gunicorn main:'create_app()'
# python -m http.server 8050
    # python main.py --command=drop-db && \
    # python main.py --command=create-db && \
    # python main.py --command=populate-db && \
    # python main.py
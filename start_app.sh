#!/bin/bash

. .venv/bin/activate && \
    python main.py --command=drop-db && \
    python main.py --command=create-db && \
    python main.py --command=populate-db && \
    python main.py
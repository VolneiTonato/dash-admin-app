#!/bin/bash

docker build . -t tonato/dash-admin-app:latest

docker push tonato/dash-admin-app:latest
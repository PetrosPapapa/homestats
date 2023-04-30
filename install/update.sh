#!/bin/bash

docker build -t homestats .
systemctl stop homestats.service
docker container rm homestats
docker create -p 7700:80 --name homestats homestats
systemctl start homestats.service
systemctl status homestats.service

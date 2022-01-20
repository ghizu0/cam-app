#!/bin/bash
cd /home/ubuntu/cam-app
sudo docker-compose build
sudo docker-compose push
sudo docker stack deploy -c docker-compose.yml

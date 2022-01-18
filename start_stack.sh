#!/bin/bash

read -p "En que modo se ejecutan las camaras c, p o f " Modo

docker-compose build
docker-compose push

modo= docker stack deploy -c docker-compose.yml

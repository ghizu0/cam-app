#!/bin/bash
docker-compose build
docker-compose push
modo= docker stack deploy -c docker-compose.yml

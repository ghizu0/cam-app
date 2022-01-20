#!/bin/bash
cd /home/ubuntu/cam-app

read -p "Introduce c (muestra imagenes), p (muestra poses) o f (toma imagenes de fondo): " modo
read -p "¿Cuantas horas va a estar en modo c o p? " horas

export compose_modo=$modo
export compose_horas=$horas

envsubst < docker-compose.yml > docker-compose-variables.yml

sudo docker stack deploy -c docker-compose-variables.yml cam-app

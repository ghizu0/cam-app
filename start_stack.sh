#!/bin/bash
cd /home/ubuntu/cam-app

export compose_horas=$1
export compose_modo=$2
export compose_modo_aseo=$2

# Aseo siempre detecta pose
if [ $2 = "c" ]
then
  export compose_modo_aseo="p"
fi

envsubst < docker-compose.yml > docker-compose-variables.yml

sudo docker stack deploy -c docker-compose-variables.yml cam-app

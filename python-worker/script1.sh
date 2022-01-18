#!/bin/sh
/bin/echo "Actualizar repositorios"
/usr/bin/apt -y update
/usr/bin/apt -y upgrade
/bin/echo "Instalar librerias:"
/usr/bin/apt install -y libjpeg-dev
/usr/bin/apt install -y mplayer fbi
/usr/bin/apt install -y feh
/usr/bin/apt install -y curl
/usr/bin/apt install -y python3-pip
/usr/bin/apt install -y python3-numpy
pip install --upgrade requests
pip install awsebcli --upgrade --user
pip install awsebcli --upgrade --user
pip install wget
pip install opencv-python
pip install mediapipe
pip install pandas
#timedatectl set-timezone Europe/Madrid
#timedatectl set-ntp on

/usr/bin/apt install -y sudo
/usr/bin/apt install -y sshpass
mkdir -p /var/www/html

curl -O https://bootstrap.pypa.io/get-pip.py
chmod +x get-pip.py

useradd -m -g sudo -s /bin/bash ubuntu
mkdir /volume

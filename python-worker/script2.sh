#!/bin/sh
python3 get-pip.py --user
echo "export PATH=~/.local/bin:$PATH" >> ~/.bashrc
. ~/.bash_logout
mkdir /home/ubuntu/pose
pip install python-dateutil
pip install attrs

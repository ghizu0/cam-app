#!/bin/bash
mkdir /volume
rm -rf /usr/share/nginx/html
ln -s /volume/$habitacion/var/www/html /usr/share/nginx/html


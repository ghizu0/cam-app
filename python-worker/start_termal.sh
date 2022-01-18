#/bin/bash
ln -s /volume/$habitacion/var/www/html/images /var/www/html/images
sshpass -e ssh -o StrictHostKeyChecking=no pi@192.168.7.246 "source /home/pi/venv/bin/activate && python3 enviar_imagen.py" &
python3 /home/ubuntu/podes_paginaweb_termal.py $cam $horas $modo

#/bin/bash
ln -s /volume/$habitacion/var/www/html/images /var/www/html/images
python3 /home/ubuntu/podes_paginaweb.py $cam $horas $modo

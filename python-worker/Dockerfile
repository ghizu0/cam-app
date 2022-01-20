FROM ubuntu:20.04

ENV TZ=Europe/Madrid
ENV SSHPASS=raspberry

USER root
ADD script1.sh /
ADD script2.sh /
RUN chmod +x /script1.sh
RUN chmod +x /script2.sh

RUN /bin/bash -c "/script1.sh"

ADD podes_paginaweb_termal.py /home/ubuntu
ADD podes_paginaweb.py /home/ubuntu
RUN chmod +x /home/ubuntu/podes_paginaweb_termal.py
RUN chmod +x /home/ubuntu/podes_paginaweb.py

USER ubuntu
RUN /bin/bash -c "/script2.sh"

USER root
ADD start.sh /
ADD start_termal.sh /
RUN chmod +x /start.sh
RUN chmod +x /start_termal.sh
ENTRYPOINT /$start_script

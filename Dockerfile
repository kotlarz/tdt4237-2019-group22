FROM nginx:1.14.0

RUN cat /etc/passwd
RUN mkdir /home/www-data \
    mkdir /home/www-data/group22
ENV APP_HOME /home/www-data/group22
WORKDIR $APP_HOME
# ExecStart=/home/www-data/group22/venv/bin/uwsgi --chdir=/home/www-data/group22/sec -w sec.wsgi:application --processes=2 --uid=33 --gid=33 --harakiri=20 --home=/home/www-data/group22/venv --http :8022 --master

ADD . $APP_HOME

COPY nginx-configuration-file /etc/nginx/nginx.conf
COPY group22.service /etc/systemd/system/

EXPOSE 4022

RUN set -e && \
    apt update && \
    apt install -y \
        python3 \
        python3-pip

RUN pip3 install virtualenv
RUN virtualenv -p python3 venv
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt
RUN python3 sec/manage.py migrate
RUN python3 sec/manage.py createsuperuser
RUN python3 sec/manage.py loaddata seed.json
CMD python3 sec/manage.py runserver


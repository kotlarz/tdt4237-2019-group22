FROM alpine

RUN apk add --no-cache dos2unix

WORKDIR /tmp

COPY ./docker-entrypoint.sh ./

RUN dos2unix ./docker-entrypoint.sh

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY --from=0 /tmp/docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
COPY seed.json create_superuser.py ./

ENTRYPOINT ./docker-entrypoint.sh

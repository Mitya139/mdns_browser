From ubuntu:23.04

RUN apt-get update
RUN apt-get install -y python3 python3-flask python3-dotenv avahi-daemon avahi-utils dbus


COPY . /app

WORKDIR /app
#RUN pip install -r /app/docker_files/requirements.txt

ENTRYPOINT /app/docker_files/entrypoint.sh


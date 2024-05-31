From ubuntu:23.04

RUN apt-get update
RUN apt-get install -y avahi-daemon avahi-utils dbus psmisc

COPY . /app

WORKDIR /app

ENTRYPOINT /app/entrypoint.sh

service dbus start


service avahi-daemon start

service avahi-daemon status

python3 -m flask --app /app/server.py run --port=5000 --host=0.0.0.0

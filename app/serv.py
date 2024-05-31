from flask import Flask, render_template
import subprocess
import threading
import time

app = Flask(__name__)

services = {}


def avahi_browse():
    while True:
        try:
            process = subprocess.Popen(['avahi-browse', '-a'], stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True)
            output, _ = process.communicate(timeout=2)
            services.clear()  # Очистить информацию о предыдущих сервисах
            for line in output.split('\n'):
                if line.strip():
                    service_info = line.split(';')
                    service_name = service_info[4]
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    services[service_name] = timestamp  # Сохранить информацию о сервисе
        except FileNotFoundError:
            print("Не удалось найти исполняемый файл avahi-browse")
        time.sleep(5)  # Пауза между сканированиями


@app.route("/")
def index():
    return render_template('index.html', services=services)


if __name__ == '__main__':
    browse_thread = threading.Thread(target=avahi_browse, daemon=True)
    browse_thread.start()

    # Запустить Flask приложение
    app.run(debug=True, port=5000)

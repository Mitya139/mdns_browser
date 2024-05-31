import argparse
import os
import random
import time
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--am', type=int, default=5, help='amount of services')
    parser.add_argument('--de', type=float, default=1, help='delay in seconds')
    return parser.parse_args()


def main():
    args = parse_arguments()
    am = args.am
    delay = args.de
    for i in range(am):
        filename = f'services/{i}.service'
        name = f'service_{i}'
        typ = f'_service{i}._tcp'
        port = random.randint(1000, 9999)
        with open(filename, 'w') as file:
            file.write(f"<service-group>\n")
            file.write(f"  <name replace-wildcards=\"yes\">{name}</name>\n")
            file.write(f"  <service protocol=\"ipv4\">\n")
            file.write(f"    <type>{typ}</type>\n")
            file.write(f"    <port>{port}</port>\n")
            file.write(f"  </service>\n")
            file.write(f"</service-group>\n")
        print(f'Service created: {name}. {datetime.fromtimestamp(time.time()).replace(microsecond=0)}')
        time.sleep(delay)

    for i in range(am):
        filename = f'services/{i}.service'
        name = f'service_{i}'
        os.remove(filename)
        print(f'Service deleted: {name}. {datetime.fromtimestamp(time.time()).replace(microsecond=0)}')
        time.sleep(delay)


if __name__ == '__main__':
    main()

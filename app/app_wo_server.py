import subprocess
import time
import csv

delay = 5
serv_data = dict()
path_all_time_data = './data/AllTimeData.csv'
path_real_time_data = './data/RealTimeData.csv'


def write_csv(data, file_path, mod):
    with open(file_path, mod, newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)


def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data


def data_control(new_data, timestamp):
    s = dict()
    for serv in new_data:
        name = serv[0] + ' ' + serv[1] + ' ' + serv[2]
        s[name] = timestamp
    if not new_data:
        s = serv_data.copy()
    for rem_serv in serv_data.keys() - s.keys():
        serv_data.pop(rem_serv)
        x = rem_serv.split()
        data = ['-'] + x[:2] + [' '.join(x[2:len(x) - 1])] + [timestamp]
        write_csv([data], path_all_time_data, 'a')

    dif = s.keys() - serv_data.keys()
    for add_serv in dif:
        serv_data[add_serv] = s[add_serv]
        x = add_serv.split()
        data = ['+'] + x[:2] + [' '.join(x[2:len(x) - 1])] + [timestamp]
        write_csv([data], path_all_time_data, 'a')

    res = []
    for i in serv_data.keys():
        res += [i.split() + [serv_data[i]]]
    res = [x[:2] + [' '.join(x[2:len(x) - 1])] + [x[-1]] for x in res]
    write_csv(res, path_real_time_data, 'w')
    return res


def avahi_browse():
    try:
        process = subprocess.Popen(['avahi-browse', '-a'], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
        try:
            output, _ = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            output, _ = process.communicate()
        output = output.split('\n')
        output = list(map(str.split, output))
        output.pop()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        output = [serv[1:-1] + [timestamp] for serv in output]
        output = [x[:2] + [' '.join(x[2:len(x) - 1])] + [x[-1]] for x in output]
        output = data_control(output, timestamp)
        print(output)
        return output
    except FileNotFoundError:
        return "The executable file could not be found"


if __name__ == '__main__':
    while True:
        avahi_browse()
        time.sleep(float(delay))

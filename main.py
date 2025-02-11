# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
import fnmatch
import os
import gzip
from string import Template
import tomllib

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "PATTERN": "nginx-access-ui.log-*"
}


def load_toml() -> dict:
    """Load TOML data from file"""
    with open('config.toml', 'rb') as f:
        toml_data: dict = tomllib.load(f)
        return toml_data


def main(conf):
    filepath_gz = ''
    filepath_raw = ''
    # Получим название и путь файла
    for file in os.listdir(conf['LOG_DIR']):
        if fnmatch.fnmatch(file, conf['PATTERN']) & fnmatch.fnmatch(file, '*.gz'):
            filepath_gz = f'{conf["LOG_DIR"]}/{file}'
            print(filepath_gz)
        elif fnmatch.fnmatch(file, conf['PATTERN']):
            filepath_raw = f'{conf["LOG_DIR"]}/{file}'
            print(filepath_raw)
    # Создадим дерикторию если нет
    if not os.path.exists(conf['REPORT_DIR']):
        os.mkdir(conf['REPORT_DIR'])
    # Получим шаблон
    html = open("templates/report.html").read()
    template = Template(html)
    # Запишем в шаблон значения и создадим файл
    if filepath_gz:
        with gzip.open(filepath_gz, mode='rb') as file_data:
            for line in file_data:
                new_line = line.decode().strip()
                print(new_line)
                return
    elif filepath_raw:
        with open(filepath_raw, mode='rb') as file_data:
            for line in file_data:
                new_line = line.decode().strip().split()
                # l = [{'count': 15844,
                #       "time_avg": 62.994999999999997,
                #       "time_max": 9843.5689999999995,
                #       "time_sum": 174306.35200000001,
                #       "url": '/export/appinstall_raw/2017-06-29/',
                #       "time_med": 60.073,
                #       "time_perc": 9.0429999999999993,
                #       "count_perc": 0.106}]
                # d = template.safe_substitute(dict(table_json=l))
                # f = open('test.html', 'a')
                # f.write(d)
                print(new_line[6])
                print(new_line[-1:])
                return


if __name__ == "__main__":
    main(config)

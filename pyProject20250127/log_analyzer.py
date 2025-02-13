# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
import argparse
import fnmatch
import gzip
import json
import os
import re
import signal
import sys
from datetime import date, datetime
from string import Template

import structlog  # type: ignore

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
}


def handler(signum, frame):
    log = structlog.stdlib.get_logger()
    log.info("Process stopped by user")
    sys.exit()


class LogHandler:
    def __init__(self, conf: dict, conf_path: str):
        self.conf_file: dict = conf
        self.pattern = "nginx-access-ui.log-*"
        self.log = structlog.stdlib.get_logger()

        if conf_path:
            try:
                with open(conf_path, "rb") as c:
                    self.conf_file = json.loads(c.read())
            except:
                self.log.error("Parse config fault")
                return

        self.report_size, self.report_dir, self.log_dir = self.conf_file.values()

        # Создадим директорию если нет
        os.makedirs(self.report_dir, exist_ok=True)

    def __get_latest_filepath(self):
        latest_file = ""
        last_date = date.__init__(self)
        # act_date = date.__init__(self)
        file_archive = False
        for file in os.listdir(self.log_dir):
            act_date = self.__get_file_date(self, file)
            if last_date is None or last_date <= act_date:
                last_date = act_date
                latest_file = file
        if fnmatch.fnmatch(latest_file, self.pattern) & fnmatch.fnmatch(
            latest_file, "*.gz"
        ):
            latest_file = f"{self.log_dir}/{latest_file}"
            file_archive = True
        elif fnmatch.fnmatch(latest_file, self.pattern):
            latest_file = f"{self.log_dir}/{latest_file}"

        return latest_file, file_archive, last_date

    @staticmethod
    def __get_file_date(self, filename) -> date:
        match_str = re.search(r"\d{4}\d{2}\d{2}", filename)
        return datetime.strptime(match_str.group(), "%Y%m%d").date()  # type: ignore

    def process_file(self):
        # Получим шаблон
        html = open("templates/report.html").read()
        template = Template(html)
        cnt = dict()
        file_path, file_archive, last_date = self.__get_latest_filepath()
        fname = f"report-{last_date.year}.{last_date.month}.{last_date.day}.html"
        url_count = request_time = 0
        total = [
            {
                "count": 0,
                "count_perc": 0,
                "time_sum": 0,
                "time_perc": 0,
                "url": "",
                "time_avg": 0,
                "time_max": 0,
                "time_med": 0,
                "all_values": [],
            }
        ]

        url_time_request: dict = {}

        self.log.info("Start process data")

        if file_archive:
            with gzip.open(file_path, mode="rb") as file_data:
                for line in file_data:
                    new_line = line.decode().strip().split()
                    self.__fill_data(
                        self,
                        url_count,
                        request_time,
                        total,
                        cnt,
                        new_line,
                        url_time_request,
                    )
        else:
            with open(file_path, mode="rb") as file_data:
                for line in file_data:
                    new_line = line.decode().strip().split()
                    self.__fill_data(
                        self,
                        url_count,
                        request_time,
                        total,
                        cnt,
                        new_line,
                        url_time_request,
                    )

        self.log.info("End process data")

        l = []
        s = dict(
            sorted(url_time_request.items(), key=lambda item: item[1], reverse=True)
        )

        for k, v in s.items():
            # Minimize report size for each line
            if self.report_size <= 0:
                break
            cnt[k][0].pop("all_values")
            l.append(cnt[k][0])
            self.report_size -= 1

        print(self.report_size)

        d = template.safe_substitute(dict(table_json=l))
        fpath = f"reports/{fname}"
        f = open(fpath, "w")
        f.write(d)

        self.log.info(f"File succesfully uploaded into {fpath}")

    @staticmethod
    def __fill_data(self, *args):
        url_count, request_time, total, cnt, new_line, url_time_request = args
        url_count += 1
        request_time += float(new_line[-1:][0])
        total.clear()

        if new_line[6] in cnt:
            curr_req_time = float(new_line[-1:][0])
            exist_line = cnt[new_line[6]]
            exist_line[0]["count"] = exist_line[0]["count"] + 1
            exist_line[0]["count_perc"] = exist_line[0]["count"] / url_count
            exist_line[0]["time_sum"] = exist_line[0]["time_sum"] + curr_req_time
            request_time = 0.1 if request_time == 0 else request_time
            exist_line[0]["all_values"][0] = exist_line[0]["all_values"][0] + float(
                new_line[-1:][0]
            )
            exist_line[0]["time_perc"] = (
                exist_line[0]["all_values"][0] / request_time * 100
            )
            exist_line[0]["time_avg"] = (
                exist_line[0]["time_sum"] / exist_line[0]["count"]
            )
            exist_line[0]["time_max"] = (
                exist_line[0]["time_max"]
                if exist_line[0]["time_max"] > curr_req_time
                else curr_req_time
            )
            exist_line[0]["time_med"] = exist_line[0]["time_med"] + 1
            total = exist_line
        else:
            total.append(
                {
                    "count": 1,
                    "count_perc": 1,
                    "time_sum": float(new_line[-1:][0]),
                    "time_perc": 1,
                    "url": new_line[6],
                    "time_avg": request_time,
                    "time_max": request_time,
                    "time_med": request_time,
                    "all_values": [float(new_line[-1:][0])],
                },
            )

        cnt[new_line[6]] = total[:]
        url_time_request[new_line[6]] = total[0]["time_perc"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="log_analyzer", description="Config file path"
    )
    parser.add_argument("-c", "--config", type=str)
    args = parser.parse_args()

    signal.signal(signal.SIGINT, handler)

    log = LogHandler(config, args.config)
    log.process_file()

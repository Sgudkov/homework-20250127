import os

from log_analyzer import LogHandler


def test_log_analyzer_config_path():
    config = {
        "REPORT_SIZE": 1000,
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log",
    }
    log = LogHandler(config, None)
    assert log.report_size is not None
    assert log.report_dir is not None
    assert log.log_dir is not None


def test_log_analyzer_file_path():
    config = {
        "REPORT_SIZE": 1000,
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log",
    }
    log = LogHandler(config, "")
    assert os.path.isfile(config["LOG_DIR"])
    file_path, file_archive, last_date = log.get_latest_filepath()
    assert file_path is not None
    assert file_archive is not None
    assert last_date is not None

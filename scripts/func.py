import re
import os
import datetime

import psutil

import logging

from logging.handlers import TimedRotatingFileHandler


def set_log(logger_name, log_file):
    rootlogger = logging.getLogger(logger_name)
    rootlogger.setLevel(logging.INFO)
    timed_rotating = TimedRotatingFileHandler(log_file,
                                       when="h",
                                       interval=1,
                                       backupCount=5,
                                       encoding='utf-8'
                                       )
    timed_rotating.setLevel(logging.INFO)
    timed_rotating.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    rootlogger.addHandler(timed_rotating)


def regex_extract(obj, config):
    regex = config['re']
    result = re.findall(regex, obj)
    return result


def remove_space(string):
    return re.sub('\s+', ' ', string)


def get_time_run(time_start, time_match):
    return (time_start + datetime.timedelta(minutes=time_match))


def convet_time_start(time_start):
    return datetime.datetime.strptime(time_start, "%Y-%m-%dT%H:%M:%S")


def get_ram():
    process_id = os.getpid()
    process = psutil.Process(process_id)
    # log_ram.warning(f"__Process id: {process_id}; Ram use: {int(process.memory_info().rss)/1024}")
    return int(process.memory_info().rss)/1024


import requests
import json
import re
import datetime
import db_handler, utils
import logging
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# use config_v3
# with open('config_v3.json', 'r', encoding='utf-8') as read_config:
#     data_config = json.load(read_config)


def get_all_key_json(obj, new_obj):
    for key, vals in obj.items():
        if isinstance(vals, str):
            new_obj[key] = vals
        elif isinstance(vals, int):
            new_obj[key] = vals
        elif isinstance(vals, dict):
            get_all_key_json(vals, new_obj)
        elif isinstance(vals, list):
            for k, v in vals.items():
                get_all_key_json(v, new_obj)
        else:
            new_obj[key] = ""
    return new_obj


def crawl_table(browser, config):
    lich_thi_dau = []
    url = config['url']
    list_table = detect_type_result(browser.xpath(config['table']['xpath']), config['table'])
    for table in list_table:
        list_row_table = detect_type_result(table.xpath(config['table']['row']['xpath']), config['table']['row'])
        for row in list_row_table:
            data_sample = config['data_sample'].copy()
            for key, val in config['data_sample'].items():
                if val == "web":
                    data = detect_type_result(html_find_xpath(browser, config[key]), config[key])
                elif val == "table":
                    data = detect_type_result(html_find_xpath(table, config['table'][key]), config['table'][key])
                elif val == "row":
                    data = detect_type_result(html_find_xpath(row, config['table']['column'][key]), config['table']['column'][key])
                else:
                    data = detect_key(key, val, data_sample, data_sample['keyword'])
                    data_sample[key] = data
                    continue
                
                if type(data) == list:
                    del data_sample[key]
                    for i in range(len(data)):
                        data_sample[key + "_" + str(i)] = data[i]
                else:
                    data_sample[key] = data
            lich_thi_dau.append(data_sample)
    return lich_thi_dau


def html_find_xpath(browser, config):
    try:
        return browser.xpath(config['xpath'])
    except:
        return ""


def detect_key(key, vals, data_sample, list_key):
    if key == "create_date":
        return datetime.datetime.now()
    elif key == "keyword":
        list_keyword = []
        for val in vals:
            try:
                list_keyword.append(data_sample[val])
            except:
                list_keyword.append(val)
        return list_keyword
    elif key == "keyword_unsign":
        list_key_unsign = []
        for key in list_key:
            try:
                list_key_unsign.append(utils.unicode_to_kodauvagach(key))
            except:
                logging.warning(data_sample)
        return list_key_unsign
    else:
        return None


def main(type, es, index_es, config):
    list_data = detect_type_response(config)
    if type == 2:
        check_update = query.update_lich_ES(es, index_es, list_data)
    elif type == 5:
        check_update = query.update_bxh_ES(es, index_es, list_data)
    return check_update


def crawl():
    pass
# def main(config):
#     list_data = detect_type_response(config)
#     print(list_data)

# with open('config_test.json', 'r', encoding='utf-8') as read_config:
#     data_config = json.load(read_config)

# main(data_config[0]['bang_xep_hang'][0])

# wc, col_config = query.connect_DB_aHuy()
# list_config = col_config.find({})
# config = list_config[0]['lich_thi_dau'][0]
# es = query.connect_ES()
# index_es = "worldcup"
# list_data = crawl_table(config)
# check_update = query.update_lich_ES(es, index_es, list_data)

# wc, col_config = query.connect_DB_aHuy()
# list_config = col_config.find({})
# config = list_config[0]['bang_xep_hang'][0]
# es = query.connect_ES()
# index_es = "worldcup"
# list_data = crawl_table(config)
# check_update = query.update_bxh_ES(es, index_es, list_data)
# print(check_update)

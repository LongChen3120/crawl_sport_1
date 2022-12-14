import sys
import datetime
sys.path.insert(0, '.\config')

import requests

import func
import config_env
import func_parse
import func_action
import func_detect
import func_request_find
import func_input_to_ouput

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def detect_type_action(browser, config, match):
    # config truyen vao la config cua doi tuong
    if config['type_action'] == 1:
        func_action.action_click(browser, config)
    elif config['type_action'] == 2:
        list_link = func_action.action_get_attribute(browser, config)
        return list_link
    elif config['type_action'] == 3:
        return func_action.action_scroll_down()
    elif config['type_action'] == 4:
        func_action.action_send_keys(browser, config, match)
    elif config['type_action'] == 5:
        return func_parse.parse_config({}, config['data'], {}, browser)
    elif config['type_action'] == 6:
        return func_action.action_enter(browser, config)


def detect_type_response(config):
    response = detect_type_crawl(config, config['url'])
    if config['type_response'] == 1:
        response = html.fromstring(response.text, 'lxml')
        list_data = func_action.parse_html(response, config)
    elif config['type_response'] == 2:
        list_data = func_action.parse_json(response.json(), config)
    return list_data


def detect_type_crawl(config, url):
    if config['type_crawl'] == 1:
        response = requests.get(url)
        return response
    elif config['type_crawl'] == 2:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.headless = False
        browser = webdriver.Chrome(executable_path='./chrome_driver/chromedriver.exe', options=options)
        browser.implicitly_wait(config_env.IMPLICITLY_WAIT)
        browser.get(url)
        return browser


def detect_type_result(result, config):
    try:
        type_result = config['type_result'] 
        if type_result == 1:
            return func_input_to_ouput.elements_to_output(result, config)
        elif type_result == 2:
            return func_input_to_ouput.list_string_to_output(result, config)
        elif type_result == 3:
            return func_input_to_ouput.list_int_to_output(result, config)
        elif type_result == 4:
            return func_input_to_ouput.string_to_output(result, config)
        elif type_result == 5:
            return func_input_to_ouput.int_to_output(result, config)
        elif type_result == 6:
            return func_input_to_ouput.datetime_to_output(result, config)
        elif type_result == 7:
            return func_input_to_ouput.timestamp_to_output(result, config)
    except:
        return None


def detect_type_find(obj, config):
    if config['type_find'] == 1: # giữ nguyên obj
        return obj
    elif config['type_find'] == 2: # tìm theo regex
        return func.regex_extract(obj, config)


def detect_time_format(time, config):
    if type(time) == list:
        time = time[0]
    time_format = config['time_format'].replace("days","%d").replace("months","%m").replace("years","%Y").replace("hours","%H").replace("minutes","%M").replace("seconds","%S").replace("microseconds", "%f")
    time = datetime.datetime.strptime(time, time_format)
    try:
        params = config['replace'].split('=')
        if params[0] == "years":
            time = time.replace(year=int(params[1]))
        elif params[0] == "months":
            time = time.replace(month=int(params[1]))
        elif params[0] == "days":
            time = time.replace(day=int(params[1]))
        elif params[0] == "hours":
            time = time.replace(hour=int(params[1]))
    except:
        pass
    return time


def detect_browser_result(browser, config):
    if config['browser_result'] == 1:
        try:
            result = func_request_find.browser_find_xpath(browser, config['xpath'])
        except:
            return None
        if config['attribute'] == 'text':
            result = result.text
        else:
            result = result.get_attribute(config['attribute'])
        result = func_detect.detect_type_result(result, config)
        return result
    elif config['browser_result'] == 2:
        try:
            results = func_request_find.browser_finds_xpath(browser, config['xpath'])
        except:
            return None
        list_result = []
        if config['attribute'] == 'text':
            for i in results:
                list_result.append(i.text)
        else:
            for i in result:
                list_result.append(i.get_attribute(config['attribute']))
        result = func_detect.detect_type_result(list_result, config)     
        return result
    elif config['browser_result'] == 3:
        try:
            results = func_request_find.browser_finds_xpath(browser, config['xpath'])
        except:
            return None
        list_result = []
        for i in results:
            temp = func_parse.parse_config({}, config['data'], {}, i)
            if temp:
                list_result.append(temp)
        return list_result

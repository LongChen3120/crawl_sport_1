import sys
sys.path.insert(0, '.\config')

import requests

import config_env

from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def send_request(url):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = False
    browser = webdriver.Chrome(executable_path=config_env.PATH_CHROME_DRIVER, options=options)
    browser.implicitly_wait(5)
    browser.get(url)
    return browser


def browser_find_xpath(browser, xpath):
    result = browser.find_element(By.XPATH, xpath)
    return result


def browser_finds_xpath(browser, xpath):
    results = browser.find_elements(By.XPATH, xpath)
    return results 



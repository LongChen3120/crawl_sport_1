import sys
import json
import time
import logging
import datetime
sys.path.insert(0, '.\config')

import func
import func_action
import func_detect
import func_request_find
import utils
import config_env
import db_handler
import crawl_lich_bxh


log_main = logging.getLogger(config_env.NAME_LOG_1)
log_ram = logging.getLogger(config_env.NAME_LOG_2)


def crawl_info_match(match, config):
    # hàm crawl detail một trận đấu
    data = {}
    step_crawl = config['step_crawl']
    for step in step_crawl:
        if step == "send_request":
            browser = func_detect.detect_type_crawl(config, config['website'])
        else:
            try:
                result = detect_step(step, browser, config, match)
                data.update(result)
            except:
                pass
    # browser.close()
    return data, browser


def crawl_loop(browser, match, config):
    data = {}
    step_crawl = config['step_crawl_loop']
    for step in step_crawl:
        try:
            result = detect_step(step, browser, config, match)
            data.update(result)
        except:
            pass
    return data


def detect_step(step, browser, config, match):
    if step == "send_key":
        key = match['detail_team_0']['name'] + " vs " + match['detail_team_1']['name']
        log_main.info("send_key")
        func_detect.detect_type_action(browser, config['send_key'], key)
    elif step == "click_search":
        log_main.info("click_search")
        func_detect.detect_type_action(browser, config['click_search'], match)
    elif step == "click_match":
        log_main.info("click_match")
        func_detect.detect_type_action(browser, config['click_match'], match)
    elif step == "click_thong_ke":
        log_main.info("click_thong_ke")
        func_detect.detect_type_action(browser, config['click_thong_ke'], match)
    elif step == "crawl_thong_ke":
        log_main.info("crawl_thong_ke")
        return func_detect.detect_type_action(browser, config['crawl_thong_ke'], match)
    elif step == "click_doi_hinh":
        log_main.info("click_doi_hinh")
        func_detect.detect_type_action(browser, config['click_doi_hinh'], match)
    elif step == "crawl_doi_hinh":
        log_main.info("crawl_doi_hinh")
        return  func_detect.detect_type_action(browser, config['crawl_doi_hinh'], match)
    elif step == "click_timelines":
        log_main.info("click_timelines")
        return  func_detect.detect_type_action(browser, config['click_timelines'], match)
    elif step == "crawl_timelines":
        log_main.info("crawl_timelines")
        return  func_detect.detect_type_action(browser, config['crawl_timelines'], match)


def format_data(match, data, config):
    # hàm format lại data theo chuẩn để lưu vào db
    data_sample = config_env.data_football_sample()
    data_sample['type'] = match['type']
    data_sample['topic'] = match['topic']
    data_sample['url'] = match['url']
    data_sample['domain'] = match['domain']
    data_sample['last_update'] = datetime.datetime.now()
    data_sample['create_date'] = match['create_date']
    data_sample['time'] = match['time']
    
    for key in data_sample:
        try:
            data_sample[key] = data[key]
        except:
            pass
    try:
        data_sample['detail_team_0'].update(data['doi_hinh_team_0'])
        data_sample['detail_team_1'].update(data['doi_hinh_team_1'])
    except:
        pass
    return data_sample
    

def crawl(id_match):
    # hàm crawl detail của một trận đấu và tự động lưu vào db
    # truyền vào id trận đấu

    # tìm kiếm trận đấu theo id
    es = db_handler.connect_ES()
    match = db_handler.find_by_id(es, config_env.INDEX_ES, id_match)

    # tìm config của trận đấu
    config = db_handler.check_config(match['_source']['topic'])

    # crawl thông tin chi tiết trận đấu
    data, browser = crawl_info_match(match['_source'], config)
    browser.close()

    # format đầu ra
    data = format_data(match['_source'], data, config)

    # lưu dữ liệu vào db
    db_handler.update_by_id(es, config_env.INDEX_ES, id_match, data)


def crawl2(id_match):
    # hàm crawl detail của một trận đấu và tự động lưu vào db
    # truyền vào id trận đấu

    # tìm kiếm trận đấu theo id
    es = db_handler.connect_ES()
    match = db_handler.find_by_id(es, config_env.INDEX_ES, id_match)

    # tìm config của trận đấu
    config = db_handler.check_config(match['_source']['topic'])

    time_crawl = 0
    try:
        # crawl thông tin chi tiết trận đấu
        log_main.info("crawl detail")
        data, browser = crawl_info_match(match['_source'], config)
        while time_crawl < 200:
            log_ram.warning(f"Start crawl: == RAM USE: {func.get_ram()} MB ==")
            try:
                # format đầu ra
                log_main.info("format data")
                data = format_data(match['_source'], data, config)

                # lưu dữ liệu vào db
                log_main.info("update to db")
                db_handler.update_by_id(es, config_env.INDEX_ES, id_match, data)
            except:
                pass
            if data['status'] == "Kết thúc":
                log_main.info("end crawl")
                log_main.info(f"data:{data}")
                break
            else:
                time.sleep(1 * 60)
                time_crawl += 1
                log_main.info(f"__loop: {time_crawl}")
                data = crawl_loop(browser, match, config)
    except:
        pass
    finally:
        browser.close()

# crawl2("4064377f826b3c990b407a8a92cf27c0")

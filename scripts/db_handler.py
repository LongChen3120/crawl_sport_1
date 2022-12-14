import sys
import json
import time
import logging
import datetime
sys.path.insert(0, '.\config')

import pymongo

# import main
import func
import config_env

from elasticsearch import Elasticsearch


def check_config(topic):
    # hàm tìm kiếm config dựa vào url
    # nhận vào url chứa domain của website
    # trả về config của website đó
    with open('./config/config_detail.json', 'r', encoding='utf-8') as rf:
        list_config = json.load(rf)
    
    for config in list_config:
        if config['topic'] == topic:
            return config
            

def connect_DB_local():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_wc = client["PaPer"]
    World_cup_2022 = db_wc["World_cup_2022"]
    config = db_wc["config_crawl_sport"]
    return World_cup_2022, config


def connect_DB_aHuy():
    client = pymongo.MongoClient("mongodb://192.168.19.168:27017")
    db_paper = client['PaPer']
    return db_paper


def connect_col_config():
    db_paper = connect_DB_aHuy()
    return db_paper['config_crawl_sport']


def insert_DB(col, list_data):
    col.insert_many(list_data)


def update_lich_DB(col, list_data):
    for match in list_data:
        filter = {"team_0":match['team_0'], "team_1":match['team_1'],"time":match['time'], "domain":match['domain']}
        if col.find_one(filter):
            vals = {"$set":match}
            col.update_one(filter, vals)
        else:
            col.insert_one(match)


def update_bxh_DB(col, list_data):
    for team in list_data:
        filter = {"group":team['group'], "team":team['team'], "domain":team['domain']}
        if col.find_one(filter):
            vals = {"$set":team}
            col.update_one(filter, vals)
        else:
            col.insert_one(team)


# def update_config():
#     wc22, col_config =connect_DB_local()
#     with open('config_v3.json', 'r', encoding='utf-8') as read_config:
#         data_config = json.load(read_config)
#     for config in data_config:
#         try:
#             if col_config.find_one({"league":config['league']}):
#                 mapping_site = {"league":{"$regex":f"{config['league']}"}}
#                 update_vals = {"$set":config}
#                 col_config.update_one(mapping_site, update_vals)
#             else:
#                 col_config.insert_one(config)
#         except:
#             print(config)
# update_config()


def connect_ES():
    es = Elasticsearch(hosts=config_env.HOST_ES)
    return es


def create_index():
    local_es = Elasticsearch(hosts=config_env.HOST_ES)
    try:
        local_es.indices.create(index=config_env.INDEX_ES)
    except:
        pass
# create_index()


def find_next_match(es, index_es):
    # search trận đấu có time > time hiện tại
    query_search = {
        "size": 1, 
        "sort": [
            {
                "time": {
                    "order": "asc"
                }
            }
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "type": 2
                        }
                    },
                    {
                        "range": {
                            "time":{
                                "gt": datetime.datetime.now()
                            }
                        }
                    }
                ]
            }
        }
    }
    match = es.search(index=index_es, body=query_search)
    return match['hits']['hits'][0]


def find_by_id(es, index_es, id):
    # tìm kiếm trận đấu theo id
    query_search = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "_id": id
                        }
                    }
                ]
            }
        }
    }
    match = es.search(index=index_es, body=query_search)
    return match['hits']['hits'][0]


def update_by_id(es, index_es, id_match, data):
    # update trận đấu theo id
    query_update = {
        "doc":data
    }
    try:
        es.update(index=index_es, id=id_match, body=query_update)
    except:
        print(data)
    

def search_doc(es, index_es, query):
    return es.search(index = index_es, body = query)


def insert_ES(es, es_index, list_data):
    for match in list_data:
        es.index(index=es_index, body=match)


def update_lich_ES(es, es_index, list_data):    
    check_update = False
    for match in list_data:
        query = {
            "query": {
                "bool": {
                    "must":[
                        {
                            "match":{
                                "type":match['type']
                            }
                        },
                        {
                            "match":{
                                "team_0":{
                                    "query":match['team_0'],
                                    "operator" : "AND"
                                }
                            }
                        },
                        {
                            "match":{
                                "team_1":{
                                    "query":match['team_1'],
                                    "operator" : "AND"
                                }
                            }
                        },
                        {
                            "match":{
                                "time":match['time']
                            }
                        },
                        {
                            "match":{
                                "domain":{
                                    "query":match['domain'],
                                    "operator": "AND"
                                }
                            }
                        }
                    ]
                }
            }            
        }
        result =  es.search(index=es_index, body=query)
        if result['hits']['total']['value'] >= 1:
            del match['create_date']
            id_match = result['hits']['hits'][0]['_id']
            query_update = {
                "doc":match
            }
            response = es.update(index=es_index, id=id_match, body=query_update)
            if response['result'] == "updated":
                # logging.warning(f"update lich ok, id:{id_match}")
                check_update = True
        else:
            # logging.warning(f"insert match id:{id_match}")
            check_update = True
            es.index(index=es_index, body=match)
    return check_update


def update_bxh_ES(es, es_index, list_data):
    check_update = False
    for team in list_data:
        query_find = {
            "query": {
                "bool": {
                    "must":[
                        {
                            "match":{
                                "group":{
                                    "query":team['group'],
                                    "operator" : "AND"
                                }
                            }
                        },
                        {
                            "match":{
                                "team":{
                                    "query":team['team'],
                                    "operator" : "AND"
                                }
                            }
                        },
                        {
                            "match":{
                                "domain":{
                                    "query":team['domain'],
                                    "operator" : "AND"
                                }
                            }
                        }
                    ]
                }
            }            
        }
        result =  es.search(index=es_index, body=query_find)
        if result['hits']['total']['value'] >= 1:
            del team['create_date']
            id_team = result['hits']['hits'][0]['_id']
            query_update = {
                "doc":team
            }
            response = es.update(index=es_index, id=id_team, body=query_update)
            if response['result'] == "updated":
                check_update = True
        else:
            es.index(index=es_index, body=team)
            check_update = True
    return check_update



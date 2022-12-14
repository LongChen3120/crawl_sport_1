from typing import Optional, Union
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, Request, Body, Form, File, UploadFile, Query
from lxml import html
from bs4 import BeautifulSoup
import requests
import uvicorn
import json

import db_handler



app = FastAPI()

# ----- GET

# check data
@app.post('/demo')
def check_data(payload:dict = None):
    es = db_handler.connect_ES()
    return db_handler.search_doc(es, "worldcup", payload)


@app.post('/get_data')
def demo(
        team_0:Optional[str] = Query(None),
        team_1:Optional[str] = Query(None),
        type:Optional[int] = Query(None),
        round:Optional[str] = Query(None),
        time:Optional[str] = Query(None),
        id:Optional[str] = Query(None)
    ):
    query_search = {
        "sort": [
            {
                "time": {
                    "order": "asc"
                }
            }
        ],
        "query":{
            "bool": {
                "must": [
                    
                ]
            }
        }
    }

    if team_0:
        query_search["query"]["bool"]["must"].append({
                                                        "match": {
                                                            "detail_team_0.name": {
                                                                "query": team_0,
                                                                "operator": "and"
                                                            }
                                                        }
                                                    })
    if team_1:
        query_search["query"]["bool"]["must"].append({
                                                        "match": {
                                                            "detail_team_1.name": {
                                                                "query": team_1,
                                                                "operator": "and"
                                                            }
                                                        }
                                                    })
    if type:
        query_search["query"]["bool"]["must"].append({
                                                        "match": {
                                                            "type":  type
                                                        }
                                                    })
    if round:
        query_search["query"]["bool"]["must"].append({
                                                        "match": {
                                                            "round": {
                                                                "query": round,
                                                                "operator": "and"
                                                            }
                                                        }
                                                    })
    if time:
        query_search["query"]["bool"]["must"].append({
                                                        "match": {
                                                            "time": {
                                                                "query": time,
                                                                "operator": "and"
                                                            }
                                                        }
                                                    })
    if id:
        query_search["query"]["bool"]["must"].append({
                                                        "match": {
                                                            "_id": id
                                                        }
                                                    })
    # return query_search
    es = db_handler.connect_ES()
    result = db_handler.search_doc(es, "worldcup", query_search)
    try:
        result['hits']['hits'][0]
        return {
            "message":"ok",
            "code": 200,
            "data":result['hits']['hits']
        }
    except:
        return {
            "message":"data not found !",
            "code": 404
        }



if __name__ == "__main__":
    uvicorn.run("api:app", host="192.168.19.163", port=8000, reload=True)
    


crawl_doi_hinh = {
            "data":{
                "doi_hinh_team_0":{
                    "position":{
                        "type_action":2,
                        "xpath":"//*[@class = 'lr-vl-hf lrvl-btrc']/*[@class = 'lrvl-tvc lrvl-f']",
                        "browser_result":1,
                        "attribute":"text",
                        "type_result":4,
                        "type_find":1,
                        "type_output":4
                    },
                    "lineups":{
                        "type_action":2,
                        "xpath":"//*[@class = 'lrvl-tlt lrvl-tl lrvl-btrc']/*[@class = 'lr-vl-ls']//*[@class = 'lrvl-pd']//span[@class = 'lrvl-pnc']",
                        "browser_result":2,
                        "attribute":"text",
                        "type_result":2,
                        "type_find":1,
                        "type_output":2
                    }
                },
                    
                "doi_hinh_team_1":{
                    "position":{
                        "type_action":2,
                        "xpath":"//*[@class = 'lr-vl-hf lrvl-bbrc']/*[@class = 'lrvl-tvc lrvl-f']",
                        "browser_result":1,
                        "attribute":"text",
                        "type_result":4,
                        "type_find":1,
                        "type_output":4
                    },
                    "lineups":[
                        {
                            "player":{
                                "type_action":2,
                                "xpath":"//*[@class = 'lrvl-tlt lrvl-tl lrvl-bbrc']/*[@class = 'lr-vl-ls']//*[@class = 'lrvl-pd']//span[@class = 'lrvl-pnc']",
                                "browser_result":2,
                                "attribute":"text",
                                "type_result":2,
                                "type_find":1,
                                "type_output":{
                                    "a":[
                                        {
                                            "g":"b"
                                        },
                                        {
                                            "f":"b"
                                        },
                                        {
                                            "f":{
                                                "gg":"dd"
                                            }
                                        }
                                    ]
                                }
                            },
                            "numb":{
                                "type_action":2,
                                "xpath":"//*[@class = 'lrvl-tlt lrvl-tl lrvl-bbrc']/*[@class = 'lr-vl-ls']//*[@class = 'lrvl-pd']//span[@class = 'lrvl-pnc']",
                                "browser_result":2,
                                "attribute":"text",
                                "type_result":2,
                                "type_find":1,
                                "type_output":2
                            }
                        }
                    ]
                }
            }
        }



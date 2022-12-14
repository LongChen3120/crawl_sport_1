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
@app.post('/info')
def check_data(payload:dict = None):
    es = db_handler.connect_ES()
    query_search = {
        "size":200,
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
    for key, vals in payload.items():
        if key == "team_0" and vals:
            query_search["query"]["bool"]["must"].append({
                                                            "match": {
                                                                "detail_team_0.name": {
                                                                    "query": vals,
                                                                    "operator": "and"
                                                                }
                                                            }
                                                        })
        if key == "team_1" and vals:
            query_search["query"]["bool"]["must"].append({
                                                            "match": {
                                                                "detail_team_1.name": {
                                                                    "query": vals,
                                                                    "operator": "and"
                                                                }
                                                            }
                                                        })
        if key == "type" and vals:
            query_search["query"]["bool"]["must"].append({
                                                            "match": {
                                                                "type":  vals
                                                            }
                                                        })
        if key == "round" and vals:
            query_search["query"]["bool"]["must"].append({
                                                            "match": {
                                                                "round": {
                                                                    "query": vals,
                                                                    "operator": "and"
                                                                }
                                                            }
                                                        })
        if key == "time" and vals:
            query_search["query"]["bool"]["must"].append({
                                                            "match": {
                                                                "time": {
                                                                    "query": vals,
                                                                    "operator": "and"
                                                                }
                                                            }
                                                        })
        if key == "id" and vals:
            query_search["query"]["bool"]["must"].append({
                                                            "match": {
                                                                "_id": vals
                                                            }
                                                        })
    # return payload
    # return query_search
    result =  db_handler.search_doc(es, "worldcup_long", query_search)
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
        "size":200,
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
    



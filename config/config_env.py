# _________________ ES _________________
# a huy : 192.168.19.168:49154
# local : http://127.0.0.1:9200/
# a hoat: http://192.168.19.77:9200/
# server: http://10.3.11.253:3008

# _________________ MongoDB _________________
# local mongodb://localhost:27017
# a huy mongodb://192.168.19.168:27017

# ______PATH_____
HOST_ES = "http://192.168.19.77:9200/"
INDEX_ES = "worldcup_long"
PATH_DB_MONGO = "mongodb://localhost:27017"
PATH_LOG_1 = "./doc/log_main/main.log"
PATH_LOG_2 = "./doc/log_ram/ram.log"
PATH_CHROME_DRIVER = "./chrome_driver/chromedriver.exe"
PATH_CONFIG = "./config/config_v2.json"


# ______VARIABLES_____
IMPLICITLY_WAIT = 5
NAME_LOG_1 = "main"
NAME_LOG_2 = "log_mem"
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
TIMEOUT = 10
TIME_RUN_SCHEDULE = 1
MAX_JOBS = 5

# ______FUNC_____
def data_football_sample():
    data = {
        "type": 0,
        "topic": "",
        "url": "",
        "domain": "",
        "create_date": "",
        "time": "",
        "last_update":"",
        "round":"",
        "group": "",
        "venue": "",
        "status":"",
        "detail_team_0": {
            "name": "",
            "ensign": "",
            "coach": "",
            "bàn thắng": "",
            "scorer": [
                {
                    "name": "",
                    "time": []
                }
            ],
            "pen":"",
            "shots": 0,
            "shot_on_target": 0,
            "possession": "",
            "passes": 0,
            "pass_accuracy": "",
            "Fouls": 0,
            "numb_yellow_cards": 0,
            "numb_red_cards": 0,
            "offsides": 0,
            "corners": 0,
            "position": "",
            "đội hình": [
                {
                    "player": "",
                    "numb": 0
                }
            ],
            "Substitutes": [
                {
                    "player": "",
                    "numb": 0
                }
            ]
        },
        "detail_team_1": {
            "name": "",
            "ensign": "",
            "coach": "",
            "bàn thắng": "",
            "scorer": [
                {
                    "name": "",
                    "time": []
                }
            ],
            "pen":"",
            "shots": 0,
            "shot_on_target": 0,
            "possession": "",
            "passes": 0,
            "pass_accuracy": "",
            "Fouls": 0,
            "numb_yellow_cards": 0,
            "numb_red_cards": 0,
            "offsides": 0,
            "corners": 0,
            "position": "",
            "đội hình": [
                {
                    "player": "",
                    "numb": 0
                }
            ],
            "Substitutes": [
                {
                    "player": "",
                    "numb": 0
                }
            ]
        },
        "substitution": [
            {
                "time": "",
                "in": [
                    {
                        "name": "",
                        "team": "",
                        "numb": 0
                    }
                ],
                "out": [
                    {
                        "name": "",
                        "team": "",
                        "numb": 0
                    }
                ]
            }
        ],
        "card": [
            {
                "time": "",
                "type_card": "",
                "player": "",
                "numb": 0,
                "team": ""
            }
        ],
        "keyword": [],
        "keyword_unsign": [],
        "thread": "",
    }
    return data
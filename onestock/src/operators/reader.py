import json
import requests
import os
import yaml
from src.operators.date import get_now, get_date
from typing import Dict

def read(file):
    f = open("/app/src/" + file)
    return json.load(f)

def get_config():
    if os.environ.get("ENV") == "prod":
        file = "config-prod.yaml"
    else:
        file = "config-staging.yaml"

    with open('/app/src/' + file) as f:
        return dict(yaml.load(f, Loader=yaml.FullLoader))

def get_creds() -> Dict[str, str]:
    secret = os.environ.get("ONESTOCK_CREDENTIALS_SECRET")
    if secret:
        return json.loads(secret)

    else:
        if "ONESTOCK_DJ_USER" not in os.environ:
            raise Exception("ONESTOCK_DJ_USER needs to be set.")

        if "ONESTOCK_DJ_PASSWORD" not in os.environ:
            raise Exception("ONESTOCK_DJ needs to be set.")

        if "ONESTOCK_CL_USER" not in os.environ:
            raise Exception("ONESTOCK_CL_USER needs to be set.")

        if "ONESTOCK_CL_PASSWORD" not in os.environ:
            raise Exception("ONESTOCK_CL_PASSWORD needs to be set.")

        return {
            "ONESTOCK_DJ_USER": os.environ["ONESTOCK_DJ_USER"],
            "ONESTOCK_DJ_PASSWORD": os.environ["ONESTOCK_DJ_PASSWORD"],
            "ONESTOCK_CL_USER": os.environ["ONESTOCK_CL_USER"],
            "ONESTOCK_CL_PASSWORD": os.environ["ONESTOCK_CL_PASSWORD"],
        }

def fetch(channel, start, min=None, max=None):
    config = get_config()
    payload = read("static/payload/payload_{}.json".format(channel))

    if min is None:
        payload["filter"]["last_update"]["min"] = get_now(config["onestock"]["delta"])
    else:
        payload["filter"]["last_update"]["min"] = get_date(min)

    if max is not None:
        payload["filter"]["last_update"]["max"] = get_date(max)

    payload["pagination"]["start"] = start
    payload["pagination"]["limit"] = config["onestock"]["limit"]

    #headers = {'Auth-User': os.environ.get("ONESTOCK_LOGIN"), 'Auth-Password': os.environ.get("ONESTOCK_PASSWORD")}
    creds = get_creds()
    ONESTOCK_DJ_USER = creds["ONESTOCK_DJ_USER"]
    ONESTOCK_DJ_PASSWORD = creds["ONESTOCK_DJ_PASSWORD"]
    ONESTOCK_CL_USER = creds["ONESTOCK_CL_USER"]
    ONESTOCK_CL_PASSWORD = creds["ONESTOCK_CL_PASSWORD"]
    
    if channel == "dj":
        headers = {'Auth-User': ONESTOCK_DJ_USER, 'Auth-Password': ONESTOCK_DJ_PASSWORD}
        r = requests.get(config["onestock"]["url"], json=payload, headers=headers)
        out = r.json()
        return out["orders"]
        
    elif channel =="cl":
        headers = {'Auth-User': ONESTOCK_CL_USER, 'Auth-Password': ONESTOCK_CL_PASSWORD}
        r = requests.get(config["onestock"]["url"], json=payload, headers=headers)
        out = r.json()
        return out["orders"]
    else:
        pass
    
    
    
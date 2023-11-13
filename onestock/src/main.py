from src.operators.reader import read, fetch
from src.operators.formatter import format, enrich
from src.operators.reader import get_config
from src.operators.logging import log
from src.operators.writer import write
from functional import seq
import traceback
import time

def ingest(min, max, kind):

    try:
        orders = list()
        table = "orders_{}".format(kind)
        keys = ["config", "item", "parcel", "item_group"]
        files = seq("static/parser/{}/config.json".format(kind), "static/parser/{}/item.json".format(kind), "static/parser/{}/parcel.json".format(kind), "static/parser/{}/item_group.json".format(kind) )\
            .map(read)\
            .list()
        schemas = dict(zip(keys, files))

        start = 1
        config = get_config()

        while start != 0:

            chain = seq(start)\
                .flat_map(lambda x: fetch(kind, x, min, max))\
                .map(lambda x: format(x, schemas["config"], schemas["item"], schemas["parcel"], schemas["item_group"]))\
                .map(enrich)  

            orders = orders + chain.list() 
           
            
            if len(chain.list()) >= config["onestock"]["limit"]:
                start = start + int(config["onestock"]["limit"])
            else:
                start = 0

            if len(orders) > config["onestock"]["batch"]:
                write(orders,table,kind)
                orders = list()
            elif start != 0:
                time.sleep(5)

        write(orders,table,kind)

        return {"result": True}

    except Exception as inst:
        traceback.print_exc()
        log()
        return {"result": False}
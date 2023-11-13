from src.operators.reader import read, fetch
from src.operators.formatter import format, enrich
from src.operators.reader import get_config
from src.operators.logging import log
from src.operators.writer import write
from functional import seq
import traceback
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

def ingest(min, max, kind):

    try:
        table = "orders_{}".format(kind)
        orders = list()
        keys = ["config", "item", "parcel", "item_group"]
        files = seq("static/parser/{}/config.json".format(kind), "static/parser/{}/item.json".format(kind), "static/parser/{}/parcel.json".format(kind), "static/parser/{}/item_group.json".format(kind) )\
            .map(read)\
            .list()
        schemas = dict(zip(keys, files))

        start = 1
        config = get_config()
        orders = list()
        
        date_format = '%Y-%m-%d'
        theDate = datetime.strptime(min, date_format)
        nextDate = theDate + relativedelta(days=7)

        while theDate < datetime.strptime(max, date_format):
            print(theDate)
            orders = list()
            while start != 0:
                #try:
                chain = seq(start)\
                        .flat_map(lambda x: fetch(kind, x, str(theDate.date()), str(nextDate.date())))\
                        .map(lambda x: format(x, schemas["config"], schemas["item"], schemas["parcel"], schemas["item_group"]))\
                        .map(enrich)  

                orders = orders + chain.list() 

                if len(chain.list()) >= config["onestock"]["limit"]:
                    start = start + int(config["onestock"]["limit"])
                    time.sleep(3)
                else:
                    start = 0

                #except Exception as inst:
                #    time.sleep(3)
                #    start = start + int(config["onestock"]["limit"])
                #    print("ERROR -> " + str(start))

            write(orders,table,kind)
            start = 1
            theDate = nextDate
            nextDate = theDate + relativedelta(days=7)
        return {"result": True}

    except Exception as inst:
        traceback.print_exc()
        log()
        return {"result": False}
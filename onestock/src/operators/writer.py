import os
from src.extensions.firestore import write as write_fs
from src.extensions.bigquery import write as write_bq

def write(orders,table_id,channel):
    if os.environ.get("ENV") == "dev":
        write_bq(orders,table_id,channel)
    else:
        write_bq(orders,table_id,channel)

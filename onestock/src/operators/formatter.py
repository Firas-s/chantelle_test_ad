from src.operators.date import get_ingestion, get_timestamp
from src.operators.refiner import *

def operate(value, order, item, parcel, group):
    if value == "get_ingestion()":
        return get_ingestion()
    elif "get_timestamp()" in value:
        return get_timestamp(get_value(order, value.split("-")[1]))
    elif "get_decimal()" in value:
        return get_decimal(order, value.split('-')[1])
    elif "get_split()" in value:
        return get_split(order, value.split('-')[1])
    elif "get_integer()" in value:
        return get_integer(order, value.split('-')[1])
    elif "get_shipping()" in value:
        return get_shipping(order, value.split('-')[1])
    elif "get_items()" in value:
        dataframe = list()
        for i in get_value(order, value.split("-")[1]):
            dataframe.append(format(i, item, None, None, None))
        return dataframe
    elif "get_parcels()" in value:
        dataframe = list()
        for i in get_value(order, value.split("-")[1]):
            dataframe.append(format(i, parcel, None, None, None))
        return dataframe
    elif "get_items_group()" in value:
        dataframe = list()
        for i in get_value(order, value.split("-")[1]):
            dataframe.append(format(i, group, None, None, None))
        return dataframe
    else:    
        return get_value(order, value)

def format(order, schema, item, parcel, group):
    dataframe = dict()
    level1_keys = schema.keys()
    for level1_key in level1_keys:
        level1_value = schema[level1_key]
        if type(level1_value) is dict:
            sub_dataframe = dict()
            for level2_key in level1_value.keys():
                level2_value = level1_value[level2_key]
                if type(level2_value) is dict:
                    sub_sub_dataframe = dict()
                    for level3_key in level2_value.keys():
                        level3_value = level2_value[level3_key]
                        sub_sub_dataframe[level3_key] = operate(level3_value, order, item, parcel, group)
                    sub_dataframe[level2_key] = sub_sub_dataframe
                else:
                    sub_dataframe[level2_key] = operate(level2_value, order, item, parcel, group)
            dataframe[level1_key] = sub_dataframe
        else:
            dataframe[level1_key] = operate(level1_value, order, item, parcel, group)

    return dataframe

def enrich(item):
    parcels = list()
    for parcel in item["parcels"]:
        parcel["items"] = list()
        for group in item["items_group"]:
            if parcel["id"] == group["parcel_id"]:
                parcel["last_update"] = group["last_update"]
                for product in item["items"]:
                    if group["item_id"] == product["id"]:
                        product["state"] = group["state"]
                        parcel["items"].append(product)
        parcel.pop("id", None)
        parcel.pop("order_id", None)
        parcels.append(parcel)
    item["parcels"] = parcels
    item.pop('items_group', None)
    return item
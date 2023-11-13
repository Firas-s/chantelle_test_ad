from decimal import *
import re

def get_value(item, key):
    if '#' in key:
        return key.replace('#', "")
    elif "." in key:
        s = key.split(".")
        for i in s:
            item = item.get(i, {})
            if not item:
                return None   
        if item == "":
            return None  
        return item
    else:
        if item.get(key) == "":
            return None  
        return item.get(key)

def get_decimal(item, key):
    value = get_value(item, key)
    if value is None:
        return None
    else:
        return round(100*float(re.sub('[^0-9\.,]', '', str(value)).replace(',', '.')))/100

def get_integer(item, key):
    value = get_value(item, key)
    if value is None:
        return None
    else:
        return int(re.sub('[^0-9]', '', str(value)))

def get_split(item, key):
    value = get_value(item, key)
    if value is None:
        return None
    else:
        return ", ".join(value)

def get_shipping(item, key):
    value = get_value(item, key)
    if value is None:
        return None
    else:
        return value[0].get("price", None)

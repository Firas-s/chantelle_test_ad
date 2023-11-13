from json import dumps
from httplib2 import Http
from src.operators.reader import get_config
from src.operators.date import get_now

def log():
    config = get_config()
    message = "Timestamp: " + str(get_now(config["onestock"]["delta"]))
    bot_message = {'text' : message}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=config["onestock"]["chat"],
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
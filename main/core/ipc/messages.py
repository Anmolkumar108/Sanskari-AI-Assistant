import json


def create_message(event, data=None):
    return json.dumps({
        "event": event,
        "data": data
    })


def parse_message(message):
    return json.loads(message)
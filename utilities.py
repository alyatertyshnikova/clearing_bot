import json


def get_token() -> str:
    with open("parameters.json", "r") as f:
        data = json.load(f)
        return data['token']
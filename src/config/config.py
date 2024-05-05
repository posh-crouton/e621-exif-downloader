import json

class Config:
    def __init__(self): 
        self.username = ""
        self.api_key= ""

def from_file(filename: str) -> Config:
    ret: Config = Config()
    with open(filename, "r") as fh:
        data = json.loads(fh.read())
    ret.username = data["username"]
    ret.api_key = data["api_key"]
    return ret

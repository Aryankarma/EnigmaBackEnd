import os

environment = os.environ.get("env")

def log(what):
    if environment == "development":
        print(what)
    


from logger import log
from chat_session import Chat
from json import dumps

def tester(*functions):
    for test_cases in functions:
        if test_cases():
            print("Passed: ", test_cases.__name__)
        else:
            print("Failed: ", test_cases.__name__)
        
        print()
        print("======================================================================")
        print()

def isDevEnv():
    import os
    return os.environ.get("env") == "development"

def test_logger():
    if not isDevEnv():
        return False
    log("Hello World")
    log("Hello World", "error")
    log("Hello World", "info")
    return True

def test_chat():
    chat = Chat("test", "gemma")
    response = chat.send_message("Hello")
    log(dumps(response.to_dict()))
    return True

if __name__=="__main__":
    tester(test_logger, test_chat)
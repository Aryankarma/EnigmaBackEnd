from logger import log
from chat_session import Chat
from json import dumps
from summarizer.utils import extract_text_from_pdf, split_text

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

def test_pdf_opener_spliter_extractor(file_name: str):
    def test_open_pdf():
        try:
            result, length = extract_text_from_pdf(file_name)
            splitted = split_text(result, length, 800)
            log()
            log()
            for i in splitted:
                print(i)
                print("\n+++++++++++++++++++++++\n")
            # log(splitted)
        except Exception as e:
            print(str(e), "error")
            return False
        return True
    return test_open_pdf

if __name__=="__main__":
    # tester(test_logger, test_chat)
    tester(test_logger, test_pdf_opener_spliter_extractor("./tmp/sample2.pdf"))
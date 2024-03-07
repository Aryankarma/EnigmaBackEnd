import ssl
import os
import json
import urllib
import requests
from summarizer.utils import extract_text_from_pdf, splittext
from dataclasses import dataclass

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def _summarize_text(text):

    allowSelfSignedHttps(True)
    data = {"inputs": text}
    body = str.encode(json.dumps(data))

    url = os.environ.get("SUMMARY_ENDPOINT_URL")
    api_key = os.environ.get("SUMMARY_ENDPOINT_KEY")

    headers = {
        'Content-Type':'application/json', 
        'Authorization':('Bearer '+ api_key), 
        'azureml-model-deployment': 'philschmid-bart-large-cnn-sa-18'
    }
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        output_string = result.decode('utf-8')
        data = json.loads(output_string)
        summary_text = data[0]["summary_text"]
        return summary_text

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        return error


def summarize(text: str, total_length: int):
    summary = ""

    if total_length > 800:
        splitted_text = splittext(text, 800)
        summary_pices = []
        for t in splitted_text:
            summary_pices.append(ollama_summarize(t))
        summary = ollama_summarize("".join(summary_pices))
    else:
        summary = _summarize_text(text)

    return summary
        

# summarize from pdf
def summarize_from_pdf(filename: str):
    finalText, totalLength = extract_text_from_pdf(filename)
    return summarize(finalText, totalLength)

@dataclass
class OllamaSummary:
    model: str
    created_at: str
    response: str
    done: str
    context: str
    total_duration: str
    load_duration: str
    prompt_eval_duration: str
    eval_count: str
    eval_duration: str

# summarize with ollama
def ollama_summarize(text: str) -> OllamaSummary: 
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": "enigma",
        "prompt": f"Summarize this text: {0}".format(text),
        "stream": False
    }

    response: OllamaSummary = requests.post(url, json=data, headers=headers).json()
    return response

if __name__=="__main__":
    summarize_from_pdf("./sample.pdf")
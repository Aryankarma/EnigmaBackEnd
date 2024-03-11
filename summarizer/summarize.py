import requests
from summarizer.utils import extract_text_from_pdf, splittext
from dataclasses import dataclass
from transformers import pipeline
from transformers import (
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer
)

import numpy as np
from transformers.pipelines import AggregationStrategy

summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

def _summarize_text(text: str):
    return summarizer(text)


class KeyphraseExtractionPipeline(TokenClassificationPipeline):

    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])

def extract_key_phrase(text: str):
    model_name = "ml6team/keyphrase-extraction-kbir-inspec"
    extractor = KeyphraseExtractionPipeline(model=model_name)
    result = extractor(text.replace("\n", " "))
    r = []

    for i in result:
        r.append(i)
    return r


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
        "model": "summarizer",
        "prompt": text,
        "stream": False
    }

    response: OllamaSummary = requests.post(url, json=data, headers=headers).json()
    return response

if __name__=="__main__":
    summarize_from_pdf("./sample.pdf")
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import summarize_from_pdf, ollama_summarize, _summarize_text, extract_key_phrase
from logger import log
from chat_session import ChatSession
from typing import Optional
from dataclasses import dataclass

app = FastAPI()

class Input(BaseModel):
    content: str


allowed_origins = ["*"]

session = ChatSession()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize_the_text(data: Input):
    summary = ollama_summarize(data.content)
    return summary

@app.post("/summarize/text")
def get_summary(data: Input):
    return _summarize_text(data.content)


@app.post("/summarize/pdf")
async def uploadAFile(file: UploadFile = File()):

    ROOT_PATH="./tmp"
    fileData = await file.read()

    with open(f"{ROOT_PATH}/{file.filename}", "bw") as writeFile:
        writeFile.write(fileData)

    summary = summarize_from_pdf(f"{ROOT_PATH}/{file.filename}")

    return {
        **summary,
        "key_entities": extract_key_phrase(summary["original_text"])
    }

    
# Chat Configuration
@dataclass
class QuestionInput(BaseModel):
    content: Optional[str] = None
    context: Optional[str] = None

@app.post("/chat/{chat_session}")
def talk(chat_session: str, inp: QuestionInput, model: Optional[str] = "llama2"):
    log(model)
    if inp.context:
        rs = session.get_chat_session(chat_session, model)
        mResponse = rs.set_context(inp.context)
        return  mResponse.message
    else:
        rs = session.get_chat_session(chat_session, model)
        mResponse = rs.send_message(inp.content)
        return  mResponse.message


@app.post("/chat/s/{chat_session}")
def talk(chat_session: str, inp: Input):
    rs = session.get_chat_session(chat_session)
    return rs.get_messages()

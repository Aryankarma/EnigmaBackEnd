from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import summarize_from_pdf, ollama_summarize, _summarize_text, extract_key_phrase
from logger import log
from chat_session import ChatSession
from typing import Optional
from dataclasses import dataclass
from uuid import uuid4

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
def get_summary(data: Input, model: Optional[str] = "llama2"):
    summary = _summarize_text(data.content)[0]["summary_text"]
    chat_session_id = uuid4()
    rs = session.get_chat_session(chat_session_id, model)
    mResponse = rs.set_context(data.content)
    log(mResponse)
    log(rs)
    return {
        "summary": summary,
        "stl": len(summary),
         "session_id": rs.get_session_id(),
        "session_context_response": mResponse.message
    }


@app.post("/summarize/pdf")
async def uploadAFile(file: UploadFile = File(), model: Optional[str] = "llama2"):

    ROOT_PATH="./tmp"
    fileData = await file.read()

    with open(f"{ROOT_PATH}/{file.filename}", "bw") as writeFile:
        writeFile.write(fileData)

    summary = summarize_from_pdf(f"{ROOT_PATH}/{file.filename}")
    chat_session_id = uuid4()

    rs = session.get_chat_session(chat_session_id, model)
    mResponse = rs.set_context(summary["original_text"])
    # log(mResponse)
    log(rs)
    return {
        **summary,
        "key_entities": extract_key_phrase(summary["original_text"]),
        "session_id": rs.get_session_id(),
        "session_context_response": mResponse
    }

    
# Chat Configuration

@app.get("/test")
def test():
    return "Hello World"


@dataclass
class QuestionInput(BaseModel):
    content: Optional[str] = None
    context: Optional[str] = None

@app.post("/chat/{chat_session}")
def talk(chat_session: str, inp: QuestionInput, model: Optional[str] = "llama2"):
    log(model)

    rs = session.get_chat_session(chat_session, model)
    mResponse = rs.send_message(inp.content)
    return  mResponse.message


@app.get("/chat/s/{chat_session}")
def talk(chat_session: str):
    rs = session.get_chat_session(chat_session)
    return {
        **rs.__dict__,
        "messages": rs.get_messages()
    }

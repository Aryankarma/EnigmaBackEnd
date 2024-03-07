from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from summarizer import summarize_from_pdf, ollama_summarize

app = FastAPI()

class SummarizeContent(BaseModel):
    content: str

@app.post("/summarize")
async def summarize_the_text(data: SummarizeContent):
    summary = ollama_summarize(data.content)
    return summary



@app.post("/summarize/pdf")
async def uploadAFile(file: UploadFile = File()):

    ROOT_PATH="./tmp"
    fileData = await file.read()

    with open(f"{ROOT_PATH}/{file.filename}", "bw") as writeFile:
        writeFile.write(fileData)

    summary = summarize_from_pdf(f"{ROOT_PATH}/{file.filename}")

    return {
        "summary": summary
    }


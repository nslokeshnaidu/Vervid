from fastapi import FastAPI, UploadFile, File

import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware
from agents.orchestrator import Orchestrator


app = FastAPI(
    title="VeriVid API",
    description="AI-powered video fact-checking system",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the orchestrator only once
orchestrator = Orchestrator()


@app.get("/")
def home():

    return {
        "project": "VeriVid",
        "status": "Backend is running"
    }


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temp_file:

        content = await file.read()

        temp_file.write(content)

        temp_path = temp_file.name

    try:

        transcript = orchestrator.speech_agent.execute(
            temp_path
        )

        return {
            "filename": file.filename,
            "transcript": transcript
        }

    finally:

        os.remove(temp_path)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temp_file:

        content = await file.read()

        temp_file.write(content)

        temp_path = temp_file.name

    try:

        result = orchestrator.analyze_video(
            temp_path
        )

        return {
            "filename": file.filename,
            "analysis": result.model_dump()
        }

    finally:

        os.remove(temp_path)
# VeriVid — AI-Powered Video Fact-Checking

VeriVid is an AI-powered video fact-checking system that analyzes spoken content in videos, extracts factual claims, retrieves supporting evidence, and evaluates whether each claim is supported, contradicted, or insufficiently supported by the available evidence.

## Features

- **Video transcription:** Converts spoken video content into text using OpenAI Whisper.
- **Claim extraction:** Uses an LLM to identify individual factual claims from the transcript.
- **Local RAG:** Retrieves relevant evidence from a locally stored knowledge base using a vector database.
- **Web evidence retrieval:** Searches the web for additional evidence related to extracted claims.
- **AI-powered verification:** Uses a locally hosted Qwen model through Ollama to classify claims.
- **Claim-by-claim review:** Displays individual claims, verdicts, explanations, and retrieved evidence.
- **Trust and coverage metrics:** Calculates a claim-support score and the percentage of claims receiving decisive verdicts.
- **Interactive web interface:** Allows users to upload videos and review the analysis through a React frontend.

## Architecture

```text
             Video Upload
                  |
                  v
          Speech Agent
             Whisper
                  |
                  v
              Transcript
                  |
                  v
        Claim Extraction Agent
          Ollama / Qwen
                  |
                  v
           Extracted Claims
                  |
          +-------+-------+
          |               |
          v               v
      Local RAG        Web Search
      Vector DB        Web Evidence
          |               |
          +-------+-------+
                  |
                  v
        Verification Agent
          Ollama / Qwen
                  |
                  v
        Claim Verdicts
                  |
                  v
            Orchestrator
                  |
                  v
          FastAPI Backend
                  |
                  v
           React Frontend
                  |
                  v
       Results and Evidence
```

## Technology Stack

| Component           | Technology                    |
| ------------------- | ----------------------------- |
| Frontend            | React, Vite, JavaScript, CSS  |
| Backend API         | Python, FastAPI               |
| Video transcription | OpenAI Whisper                |
| Language model      | Qwen via Ollama               |
| Embeddings          | Sentence Transformers         |
| Retrieval           | Local RAG and vector database |
| Web evidence        | DDGS web search               |
| API documentation   | FastAPI / Swagger UI          |
| Version control     | Git and GitHub                |

## Project Structure

```text
VeriVid/
├── backend/
│   ├── agents/
│   │   ├── speech_agent.py
│   │   ├── claim_extraction_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── verification_agent.py
│   │   └── orchestrator.py
│   ├── services/
│   │   ├── document_ingestion.py
│   │   ├── vector_db.py
│   │   └── web_search.py
│   ├── models/
│   ├── data/
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
├── data/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── index.html
└── README.md
```

_The structure above highlights the main components; filenames and folders may vary in the current implementation._

## Prerequisites

Install the following before running VeriVid:

- Python and pip
- Node.js and npm
- Ollama
- Git

The backend also requires its Python dependencies and the embedding model used by the local retrieval service.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ns lokeshnaidu/VeriVid.git
cd VeriVid
```

If the clone command fails, use the exact repository URL shown on your GitHub page.

### 2. Set up the backend

Open a terminal in the backend directory:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set up Ollama

Install and start Ollama, then download the model used by the application:

```bash
ollama pull qwen3:1.7b
```

Ensure Ollama is running before analyzing a video.

### 4. Start the backend

From the `backend` directory, run:

```bash
uvicorn main:app --reload
```

The backend should be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

### 5. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, usually http://localhost:5173.

Keep both the backend and frontend running while using the application.

## API Endpoints

| Method | Endpoint      | Purpose                                        |
| ------ | ------------- | ---------------------------------------------- |
| GET    | `/`           | Checks backend availability                    |
| POST   | `/transcribe` | Uploads a video and returns its transcript     |
| POST   | `/analyze`    | Runs the complete video fact-checking pipeline |

For interactive requests, open the Swagger documentation at `/docs` and upload a supported video file.

## Verdict Definitions

- **SUPPORTED:** The retrieved evidence supports the factual claim.
- **CONTRADICTED:** The retrieved evidence conflicts with the factual claim.
- **INSUFFICIENT:** The available evidence does not establish whether the claim is true or false.

The claim-support score is calculated from decisive verdicts, while coverage measures the proportion of analyzed claims receiving a decisive verdict. These are system-generated metrics, not guarantees of factual accuracy.

## Current Limitations

- Transcription accuracy depends on audio quality, accents, background noise, and the selected Whisper model.
- Claim extraction may omit claims or incorrectly interpret speech.
- Search results and local documents may be incomplete, outdated, or irrelevant.
- LLM-generated verdicts and explanations can be incorrect.
- The current version focuses on spoken content and evidence retrieval rather than comprehensive visual analysis of video frames.
- The trust score should be interpreted as a heuristic metric, not a statistically calibrated probability that a video is truthful.

## Future Improvements

- Improve claim extraction completeness and transcription quality.
- Improve evidence relevance, source quality, and ranking.
- Add multilingual transcription and claim verification.
- Add video-frame analysis and OCR.
- Develop a more rigorous evaluation dataset and calibrated confidence measures.

## Disclaimer

VeriVid is an experimental AI-assisted fact-checking project intended for educational and research purposes. Its results should not be treated as definitive proof of truth or falsehood. Important claims should be checked against reliable primary sources.

## Author

**Lokesh Naidu**

GitHub: https://github.com/nslokeshnaidu

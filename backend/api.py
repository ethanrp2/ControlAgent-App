from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from runner import run_control_agent
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvalRequest(BaseModel):
    dataset_dir: str = "./ControlEval/"
    dataset_files: list[str] | None = None

@app.post("/api/evaluate")
def evaluate(req: EvalRequest):
    try:
        result = run_control_agent(dataset_dir=req.dataset_dir, dataset_files=req.dataset_files)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
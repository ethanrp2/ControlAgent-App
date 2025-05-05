# backend/api.py
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from ws_manager import WebSocketManager

from runner import run_control_agent_from_inputs

load_dotenv()

app = FastAPI(title="ControlAgent Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # lock this down to your vercel domain in production
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
ws_manager = WebSocketManager()

class EvalRequest(BaseModel):
    num:              list[float] = Field(..., description="Numerator coeffs, e.g. [b0]")
    den:              list[float] = Field(..., description="Denominator coeffs, e.g. [a0, a1]")
    tau:              float | None = Field(None, description="Optional time delay")
    phase_margin_min: float        = Field(..., description="Min required phase margin (deg)")
    settling_time_min: float       = Field(..., description="Min settling time (s)")
    settling_time_max: float       = Field(..., description="Max settling time (s)")
    steadystate_error_max: float   = Field(..., description="Max steady-state error")
    scenario:         str | None   = Field("custom", description="Scenario tag")

class EvalResponse(BaseModel):
    success: bool
    data:    dict

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # optional keep-alive, no-op
    except Exception:
        ws_manager.disconnect(websocket)

@app.post("/api/evaluate", response_model=EvalResponse)
async def evaluate(req: EvalRequest):
    try:
        async def progress_callback(message: str):
            await ws_manager.broadcast(message)

        result = run_control_agent_from_inputs(req.model_dump(), progress_callback)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

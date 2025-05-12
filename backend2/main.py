import asyncio
import traceback
from typing import List, Optional
from collections import deque

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from starlette.websockets import WebSocket, WebSocketDisconnect

from api.task import CompleteTaskResp, complete_task
from model.control_task import TaskSpecs, TaskDesignResult

load_dotenv()

app = FastAPI(title="ControlAgent Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down to your vercel domain in production
    allow_credentials=True,
    allow_headers=["*"],
)

MAX_REQUEST_HISTORY_SIZE = 100 # store 100 user requests
request_history_cache: deque[TaskSpecs] = deque(maxlen=MAX_REQUEST_HISTORY_SIZE)


@app.post("/api/complete_task", response_model=CompleteTaskResp)
async def handle_complete_task(specs: TaskSpecs):
    request_history_cache.append(specs)
    print(f"Request added to history cache (POST). Cache size: {len(request_history_cache)}")
    return await complete_task(specs)


async def _queue_iter(q: asyncio.Queue):
    while True:
        item = await q.get()
        yield item
        q.task_done()


@app.websocket("/api/complete_task")
async def handle_complete_task_websocket(websocket: WebSocket):
    await websocket.accept()
    task_spec_data = await websocket.receive_json()
    task_spec = TaskSpecs.parse_obj(task_spec_data)
    print("Received task spec:", task_spec)

    request_history_cache.append(task_spec)
    print(f"Request added to history cache (WebSocket). Cache size: {len(request_history_cache)}")

    result_chan: asyncio.Queue[TaskDesignResult] = asyncio.Queue()
    design_task = asyncio.create_task(complete_task(task_spec, _async=True, result_queue=result_chan))
    print("start design task")

    async def forward_to_client():
        try:
            async for cur_result in _queue_iter(result_chan):
                print("Send result to client:", cur_result)
                await websocket.send_json(cur_result.model_dump(mode="json"))
                if cur_result.conversation_round == -1:
                    await websocket.close(code=1000, reason="Task completed")
                    break
        except asyncio.CancelledError:
            return

    forward_task = asyncio.create_task(forward_to_client())
    print("start forwarding task")

    try:
        await asyncio.gather(design_task, forward_task)
        print("Finished task")
        # receive further instruction from FE
        # while True:
        #     await websocket.receive_json()
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print("Encountered an exception:", e)
        traceback.print_exc()
        await websocket.close(code=1011, reason=str(e))
    finally:
        print("request exit")
        design_task.cancel()
        forward_task.cancel()


@app.get("/api/requests/history", response_model=List[TaskSpecs])
async def get_request_history():
    """
    Retrieves the recent history of TaskSpecs requests stored in memory.
    The history is limited to the last MAX_REQUEST_HISTORY_SIZE requests.
    """
    return list(request_history_cache)


@app.get("/api/requests/history/{index}", response_model=TaskSpecs)
async def get_request_history_by_index(
    index: int = Path(..., title="Index of the request in cache", ge=0)
):
    current_cache_size = len(request_history_cache)
    if index >= current_cache_size:
        raise HTTPException(status_code=404, detail=f"Index {index} out of bounds. Cache currently has {current_cache_size} items.")
    try:
        if index < 0:
             raise HTTPException(status_code=400, detail="Index must be a non-negative integer.")
        return request_history_cache[index]
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Request at index {index} not found.")


@app.get("/api/requests/history/range/", response_model=List[TaskSpecs])
async def get_request_history_by_range(
    left_pos: int = Query(..., title="Start index of the range (inclusive)", ge=0),
    right_pos: int = Query(..., title="End index of the range (inclusive)", ge=0)
):
    if left_pos > right_pos:
        return []

    current_cache_size = len(request_history_cache)
    
    actual_left = max(0, left_pos)
    actual_right = min(current_cache_size, right_pos + 1)

    if actual_left >= actual_right:
        return []

    return list(request_history_cache)[actual_left:actual_right]
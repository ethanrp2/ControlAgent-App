from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            try:
                await websocket.close()
            except Exception:
                pass  # Already closed or closing

    async def broadcast(self, message: str):
        for websocket in self.active_connections.copy():
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                await self.disconnect(websocket)
            except Exception:
                await self.disconnect(websocket)
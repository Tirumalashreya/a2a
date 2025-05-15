from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Callable, Dict, Any
import asyncio

class JSONRPCHandler:
    def __init__(self, tasks: Dict[str, Callable], agent_card: Dict[str, Any]):
        self.tasks = tasks
        self.agent_card_data = agent_card

    async def endpoint(self, request: Request) -> JSONResponse:
        req_data = await request.json()
        method = req_data.get("method")
        params = req_data.get("params", {})
        req_id = req_data.get("id")

        task_func = self.tasks.get(method)
        if task_func is None:
            return JSONResponse({"jsonrpc": "2.0", "error": "Unknown method", "id": req_id})

        if asyncio.iscoroutinefunction(task_func):
            result = await task_func(params)
        else:
            result = task_func(params)

        return JSONResponse({"jsonrpc": "2.0", "result": result, "id": req_id})

    async def agent_card(self, request: Request) -> JSONResponse:
        return JSONResponse(self.agent_card_data)

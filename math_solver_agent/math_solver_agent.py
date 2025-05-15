import os
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
import httpx
import asyncio
import json_rpc
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

async def call_gemini_llm(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {str(e)}"

async def call_calculator_agent(expression: str) -> str:
    async with httpx.AsyncClient() as client:
        payload = {
            "jsonrpc": "2.0",
            "method": "a2a.task",
            "params": {"input": expression},
            "id": "calc-1"
        }
        try:
            resp = await client.post("http://localhost:8001/a2a", json=payload, timeout=10.0)
            resp_json = resp.json()
            return resp_json.get("result", {}).get("output", "No result from calculator agent")
        except Exception as e:
            return f"Calculator agent call failed: {str(e)}"

async def math_solver_handler(request: Request):
    try:
        data = await request.json()
    except Exception:
        error = json_rpc.JsonRpcError(json_rpc.ERROR_CODES["PARSE_ERROR"], "Invalid JSON")
        return JSONResponse(json_rpc.make_error_response(error), status_code=400)

    try:
        requests = json_rpc.parse_request(data)
    except json_rpc.JsonRpcError as e:
        return JSONResponse(json_rpc.make_error_response(e), status_code=400)

    responses = []
    for req in requests:
        if json_rpc.is_notification(req):
            continue

        if req.get("method") != "a2a.task":
            error = json_rpc.JsonRpcError(json_rpc.ERROR_CODES["METHOD_NOT_FOUND"], "Method not found", id=req.get("id"))
            responses.append(json_rpc.make_error_response(error))
            continue

        input_text = req.get("params", {}).get("input", "")

        prompt = f"""
        You are a helpful math assistant. Solve the following problem:
        {input_text}

        If you need to perform a calculation, respond with "CALCULATE: <expression>"
        Otherwise, respond with the final solution only.
        """

        llm_response = await call_gemini_llm(prompt)

        if llm_response.startswith("CALCULATE:"):
            expression = llm_response[len("CALCULATE:"):].strip()
            calc_result = await call_calculator_agent(expression)
            final_answer = f"Result: {calc_result}"
        else:
            final_answer = llm_response

        response = json_rpc.make_response({"output": final_answer}, req.get("id"))
        responses.append(response)

    resp_data = json_rpc.batch_response(responses)
    return JSONResponse(resp_data if resp_data else {}, status_code=200)

app = Starlette(routes=[Route("/a2a", math_solver_handler, methods=["POST"])])

if __name__ == "__main__":
    import uvicorn
    print("Starting Math Solver Agent on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

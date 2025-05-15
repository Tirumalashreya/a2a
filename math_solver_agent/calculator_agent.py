from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from sympy import sympify


import json_rpc

async def calculator_handler(request: Request):
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

        expression = req.get("params", {}).get("input", "")
        try:
            result = sympify(expression)
            output = str(result)
        except Exception as e:
            output = f"Error: {str(e)}"

        response = json_rpc.make_response({"output": output}, req.get("id"))
        responses.append(response)

    resp_data = json_rpc.batch_response(responses)
    return JSONResponse(resp_data if resp_data else {}, status_code=204)

app = Starlette(routes=[Route("/a2a", calculator_handler, methods=["POST"])])

if __name__ == "__main__":
    import uvicorn
    print("Starting Calculator Agent on port 8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)

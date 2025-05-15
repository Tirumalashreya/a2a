import json

JSONRPC_VERSION = "2.0"

ERROR_CODES = {
    "PARSE_ERROR": -32700,
    "INVALID_REQUEST": -32600,
    "METHOD_NOT_FOUND": -32601,
    "INVALID_PARAMS": -32602,
    "INTERNAL_ERROR": -32603,
}

class JsonRpcError(Exception):
    def __init__(self, code, message, data=None, id=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data
        self.id = id

    def to_dict(self):
        err = {
            "code": self.code,
            "message": self.message,
        }
        if self.data is not None:
            err["data"] = self.data
        return {
            "jsonrpc": JSONRPC_VERSION,
            "error": err,
            "id": self.id
        }

def parse_request(data):
    if isinstance(data, list):
        if len(data) == 0:
            raise JsonRpcError(ERROR_CODES["INVALID_REQUEST"], "Empty batch", id=None)
        return [validate_request(req) for req in data]
    elif isinstance(data, dict):
        return [validate_request(data)]
    else:
        raise JsonRpcError(ERROR_CODES["INVALID_REQUEST"], "Invalid JSON-RPC request format", id=None)

def validate_request(req):
    if not isinstance(req, dict):
        raise JsonRpcError(ERROR_CODES["INVALID_REQUEST"], "Request must be an object", id=None)
    if req.get("jsonrpc") != JSONRPC_VERSION:
        raise JsonRpcError(ERROR_CODES["INVALID_REQUEST"], "Invalid JSON-RPC version", id=req.get("id"))
    if "method" not in req or not isinstance(req["method"], str):
        raise JsonRpcError(ERROR_CODES["INVALID_REQUEST"], "Missing or invalid method", id=req.get("id"))
    if "params" in req and not isinstance(req["params"], (list, dict)):
        raise JsonRpcError(ERROR_CODES["INVALID_PARAMS"], "Invalid params", id=req.get("id"))
    return req

def make_response(result, id):
    return {
        "jsonrpc": JSONRPC_VERSION,
        "result": result,
        "id": id
    }

def make_error_response(error: JsonRpcError):
    return error.to_dict()

def is_notification(req):
    return "id" not in req or req["id"] is None

def batch_response(responses):
    if not responses:
        return None
    return responses if len(responses) > 1 else responses[0]

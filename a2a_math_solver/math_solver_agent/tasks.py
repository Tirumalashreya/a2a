import httpx
from typing import Dict

async def solve_math_question(task_input: Dict) -> Dict:
    question = task_input.get("question")
    expression = question.replace("What is", "").replace("?", "").strip()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8001/", json={
            "jsonrpc": "2.0",
            "method": "math/calculate",
            "params": {"expression": expression},
            "id": 1
        })
        result = response.json().get("result")
    return {"answer": result}

TASKS = {
    "math/solve": solve_math_question
}

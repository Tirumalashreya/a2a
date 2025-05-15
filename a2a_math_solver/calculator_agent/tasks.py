from typing import Dict

def calculate(task_input: Dict) -> Dict:
    expression = task_input.get("expression")
    try:
        result = eval(expression)  # WARNING: Only safe for controlled inputs
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

TASKS = {
    "math/calculate": calculate
}
